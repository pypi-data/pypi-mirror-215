import logging
import time
import numpy as np

from pyfairsim.sim_algorithm.SIM_Utils import (
    run_reconstruction,
    estimate_parameters,
    estimate_absolute_phases_parallel,
    plot_img,
)
from pyfairsim.sim_algorithm.SIM_Parameters import Parameters

from pyfairsim.utils.argparse import parse_args_reconstruction
from pyfairsim.utils.load_settings import load_settings, save_settings
from pyfairsim.utils.tif import (
    load_tif,
    order_images,
    tile_images,
    fft_images,
    fade_border_cos,
    stitch_tiles,
    save_tif,
    tif_basename,
)


def main():
    args = parse_args_reconstruction()

    #logging.basicConfig(level=args.level)
    
    logging.basicConfig(filename= tif_basename(args.filename) + "_tiled.log", encoding='utf-8', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    global logger
    logger = logging.getLogger()

    print(f"Running tiled reconstruction for {args.filename}")

    if args.settings_filename:
        logger.debug(f"loading settings from {args.settings_filename}")
        settings = load_settings(args.settings_filename)
    else:
        logger.warning(f"no settings provided fall back on default settings")
        settings = load_settings(args.filename)

    # copy the settings to keep a reference of the global k-vectors and phases
    global_settings = Parameters.from_dict(settings.as_dict())

    logger.debug(f"loading images from {args.filename}")
    images, _ = load_tif(args.filename)

    if len(images) < len(settings.directions) * settings.directions[0].number_phases:
        logger.error(
            f"given image stack has to few images n={len(images)} but at least {len(settings.directions) * settings.directions[0].number_phases} are expected"
        )
        return

    logger.debug(f"order images")
    ordered_images = order_images(
        images,
        len(settings.directions),
        settings.directions[0].number_phases,
        settings.image_parameters.ordering,
        settings.image_parameters.z_slice,
    )
    # fade all images because the fading before fft is only done on the tiles and not on the whole image
    for image in ordered_images:
        image = fade_border_cos(image, 15)

    logger.debug(f"tiling images")
    logger.setLevel(logging.INFO)
    # ToDo is it good to have full overlap?
    overlap = settings.image_parameters.tile_size//2
    relative_size = (settings.image_parameters.tile_size + overlap) / global_settings.image_parameters.image_shape[0]
    tiles = tile_images(ordered_images, settings.image_parameters.tile_size, overlap)
    results = []

    start = time.time()
    settings.image_parameters.image_shape = (settings.image_parameters.tile_size + overlap, settings.image_parameters.tile_size + overlap)
    logger.info(f"reconstructing a total of {len(tiles) + 1} tiles with shape {settings.image_parameters.image_shape} including an overlap of {overlap}")
    for direction_number, direction in enumerate(settings.directions):
        logger.info(f"global k-vector for direction {direction_number}: ({direction.px*relative_size}, {direction.py*relative_size})")
        logger.info(f"with phases: {direction.phases}")
    for tile_number, tile_stack in enumerate(tiles):

        logger.debug(f"fft images on tile {tile_number}")
        raw_images = fft_images(
            tile_stack,
            len(settings.directions),
            settings.directions[0].number_phases,
            settings.image_parameters.background,
            pixels_to_fade=overlap-1
        )
        logger.info(f"run k-vector estimation on tile {tile_number}")
        estimate_parameters(settings, raw_images, False)
        for direction_number, (direction, direction_global) in enumerate(zip(settings.directions, global_settings.directions)):
            # ToDo what is a good range where we can assume that the k-vector is ok
            if (np.abs(direction.px - direction_global.px*relative_size) > 1 or np.abs(direction.py - direction_global.py*relative_size) > 1):
                logger.warning(f"k-vector estimation failed for direction {direction_number} and tile {tile_number} using global k-vector instead")
                direction.px = direction_global.px*relative_size
                direction.py = direction_global.py*relative_size
        estimate_absolute_phases_parallel(settings, raw_images)
        # ToDo what if phase estimation fails?

        logger.info(f"run reconstruction on tile {tile_number}")
        result = run_reconstruction(settings, raw_images)
        results.append(result[0])
    shape = (2 * images[0].shape[0], 2 * images[0].shape[1])
    result = stitch_tiles(results, 2 * settings.image_parameters.tile_size, shape, 2 * overlap)
    stop = time.time()
    logger.info(f"reconstruction done in {stop-start:.2f} s.")

    if args.out_filename:
        save_tif(result, args.out_filename)
        # widefield_filename = tif_basename(args.out_filename) + "_filtered_widefield.tif"
        # save_tif(result[1], widefield_filename)
    else:
        plot_img(result, "reconstructed image")
        # plot_img(result[1], "filtered widefield")


if __name__ == "__main__":
    main()
