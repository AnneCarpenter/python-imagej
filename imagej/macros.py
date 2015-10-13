import javabridge
from cellprofiler.preferences import get_headless


def get_commands():
    '''Return a list of the available command strings'''
    hashtable = javabridge.static_call('ij/Menus', 'getCommands',
                              '()Ljava/util/Hashtable;')
    if hashtable is None:
        #
        # This is a little bogus, but works - trick IJ into initializing
        #
        execute_command("pleaseignorethis")
        hashtable = javabridge.static_call('ij/Menus', 'getCommands',
                                  '()Ljava/util/Hashtable;')
        if hashtable is None:
            return []
    keys = javabridge.call(hashtable, "keys", "()Ljava/util/Enumeration;")
    keys = javabridge.jenumeration_to_string_list(keys)
    values = javabridge.call(hashtable, "values", "()Ljava/util/Collection;")
    values = [javabridge.to_string(x) for x in javabridge.iterate_java(
        javabridge.call(values, 'iterator', "()Ljava/util/Iterator;"))]

    class CommandList(list):
        def __init__(self):
            super(CommandList, self).__init__(keys)
            self.values = values

    return CommandList()


def execute_command(command, options=None):
    '''Execute the named command within ImageJ'''
    if options is None:
        javabridge.static_call("ij/IJ", "run", "(Ljava/lang/String;)V", command)
    else:
        javabridge.static_call("ij/IJ", "run",
                      "(Ljava/lang/String;Ljava/lang/String;)V",
                      command, options)


def execute_macro(macro_text):
    '''Execute a macro in ImageJ
    
    macro_text - the macro program to be run
    '''
    interp = javabridge.make_instance("ij/macro/Interpreter", "()V");
    javabridge.execute_runnable_in_main_thread(javabridge.run_script(
        """new java.lang.Runnable() {
        run: function() {
            interp.run(macro_text);
        }}""", dict(interp=interp, macro_text=macro_text)), synchronous=True)


def run_batch_macro(macro_text, imp):
    '''Run a macro in batch mode
    
    macro_text - the macro program to be run
    imp - an image plus to become the active image
    
    returns the image plus that was the active image at the end of the run
    '''
    script = """
    new java.util.concurrent.Callable() {
        call: function() {
             return interp.runBatchMacro(macro_text, imp);
        }
    };
    """
    interp = javabridge.make_instance("ij/macro/Interpreter", "()V");
    future = javabridge.make_future_task(javabridge.run_script(
        script, dict(interp=interp, macro_text=macro_text, imp=imp)))
    return javabridge.execute_future_in_main_thread(future)


def get_user_loader():
    '''The class loader used to load user plugins'''
    return javabridge.static_call("ij/IJ", "getClassLoader", "()Ljava/lang/ClassLoader;")


def get_plugin(classname):
    '''Return an instance of the named plugin'''
    if classname.startswith("ij."):
        cls = javabridge.class_for_name(classname)
    else:
        cls = javabridge.class_for_name(classname, get_user_loader())
    cls = javabridge.get_class_wrapper(cls, True)
    constructor = javabridge.get_constructor_wrapper(cls.getConstructor(None))
    return constructor.newInstance(None)


if __name__ == "__main__":
    import sys

    javabridge.attach()
    try:
        commands = get_commands()
        print "Commands: "
        for command in commands:
            print "\t" + command
        if len(sys.argv) == 2:
            execute_command(sys.argv[1])
        elif len(sys.argv) > 2:
            execute_command(sys.argv[1], sys.argv[2])

    finally:
        javabridge.detach()
        javabridge.kill_vm()
