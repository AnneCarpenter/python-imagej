import javabridge


def get_image(imageprocessor_obj, do_scaling=False):
    '''Retrieve the image from an ImageProcessor
    
    Returns the image as a numpy float array.
    '''
    #
    # The strategy is:
    # * Make a TypeConverter
    # * Ask the TypeConverter for a float ImageProcessor
    # * Get the pixels - should be a float array
    #
    type_converter = javabridge.make_instance(
        'ij/process/TypeConverter', '(Lij/process/ImageProcessor;Z)V',
        imageprocessor_obj, do_scaling)
    float_processor = javabridge.call(
        type_converter, 'convertToFloat', '([F)Lij/process/ImageProcessor;',
        None)
    jpixels = javabridge.call(
        float_processor, 'getPixels', '()Ljava/lang/Object;')
    pixels = javabridge.get_env().get_float_array_elements(jpixels)
    height = javabridge.call(imageprocessor_obj, 'getHeight', '()I')
    width = javabridge.call(imageprocessor_obj, 'getWidth', '()I')
    pixels.shape = (height, width)
    return pixels


def make_image_processor(array):
    '''Create an image processor from the given image
    
    array - an array that will be cast to double. Values should be
            between 0 and 255
    '''
    return javabridge.make_instance(
        'ij/process/FloatProcessor', '(II[D)V',
        array.shape[1], array.shape[0], array)
