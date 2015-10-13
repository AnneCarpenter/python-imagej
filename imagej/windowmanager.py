import javabridge
import imagej.imageplus


def get_current_image():
    '''Get the WindowManager's current image
    
    returns a wrapped ImagePlus object
    '''
    #
    # Run this on the UI thread so its thread context is the same
    # as the macro invocation
    #
    script = """
    new java.util.concurrent.Callable() {
        call: function() {
            return Packages.ij.WindowManager.getCurrentImage();
        }
    };
    """
    gci = javabridge.make_future_task(javabridge.run_script(script))
    imageplus_obj = javabridge.execute_future_in_main_thread(gci)
    return imagej.imageplus.get_imageplus_wrapper(imageplus_obj)


def get_id_list():
    '''Get the list of IDs of open images'''
    jid_list = javabridge.get_env().get_int_array_elements(
        javabridge.static_call('ij/WindowManager', 'getIDList', '()[I'))
    return jid_list


def get_image_by_id(imagej_id):
    '''Get an ImagePlus object by its ID'''
    return imagej.imageplus.get_imageplus_wrapper(javabridge.static_call(
        'ij/WindowManager', 'getImage', '(I)Lij/ImagePlus;', imagej_id))


def get_image_by_name(title):
    '''Get the ImagePlus object whose title (in the window) matches "title"'''
    return imagej.imageplus.get_imageplus_wrapper(javabridge.static_call(
        'ij/WindowManager', 'getImage', '(Ljava/lang/String;)Lij/ImagePlus;',
        title))


def get_temp_current_image():
    '''Get the temporary ImagePlus object for the current thread'''
    script = """
    new java.util.concurrent.Callable() {
        call: function() {
            return Packages.ij.WindowManager.getTempCurrentImage();
        }
    };
    """
    gtci = javabridge.make_future_task(javabridge.run_script(script))
    imageplus_obj = javabridge.execute_future_in_main_thread(gtci)
    return imagej.imageplus.get_imageplus_wrapper(imageplus_obj)


def make_unique_name(proposed_name):
    '''Create a unique title name for an imageplus object'''
    return javabridge.static_call('ij/WindowManager', 'makeUniqueName',
                         '(Ljava/lang/String;)Ljava/lang/String;',
                         proposed_name)


def set_temp_current_image(imagej_obj):
    '''Set the temporary current image for the UI thread'''
    script = """
    new java.lang.Runnable() {
        run: function() {
            Packages.ij.WindowManager.setTempCurrentImage(ip);
        }
    };
    """
    javabridge.execute_runnable_in_main_thread(
        javabridge.run_script(script, dict(ip=imagej_obj.o)), True)


def set_current_image(imagej_obj):
    '''Set the currently active window
    
    imagej_obj - an ImagePlus to become the current image
    '''
    javabridge.execute_runnable_in_main_thread(javabridge.run_script(
        """new java.lang.Runnable() {
            run:function() {
                var w = imp.getWindow();
                if (w == null) {
                    imp.show();
                } else {
                    Packages.ij.WindowManager.setCurrentWindow(w);
                }
            }
        }
        """, dict(imp=imagej_obj.o)), synchronous=True)


def close_all_windows():
    '''Close all ImageJ windows
    
    Hide the ImageJ windows so that they don't go through the Save dialog,
    then call the Window Manager's closeAllWindows to get the rest.
    '''
    jimage_list = javabridge.static_call('ij/WindowManager', 'getIDList', '()[I')
    if jimage_list is None:
        return
    image_list = javabridge.get_env().get_int_array_elements(jimage_list)
    for image_id in image_list:
        ip = javabridge.static_call('ij/WindowManager', 'getImage',
                           '(I)Lij/ImagePlus;', image_id)
        ip = imagej.imageplus.get_imageplus_wrapper(ip)
        ip.hide()
    javabridge.static_call('ij/WindowManager', 'closeAllWindows', '()Z')
