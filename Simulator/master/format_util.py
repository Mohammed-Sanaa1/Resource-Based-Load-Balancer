#TO BE IMPLEMENTED: helper functions that simplify print formatting using escape sequences

#tf = text_format
class tf:
    NORMAL              ="\033[0;"
    BOLD                ="\033[1;"
    ITALIC              ="\033[3;"
    UNDERLINE           ="\033[4;"
    BLINK               ="\033[5;"
    INVERSE             ="\033[7;"
    RESET               ="\033[0m"

    RED                 ="31"
    GREEN               ="32"
    YELLOW              ="33"
    BLUE                ="34"
    MAGENTA             ="35"
    CYAN                ="36"
    WHITE               ="37"
    GRAY                ="90"
    GREY                ="90"
    BRIGHTRED           ="91"
    BRIGHTGREEN         ="92"
    BRIGHTYELLOW        ="93"
    BRIGHTBLUE          ="94"
    BRIGHTMAGENTA       ="95"
    BRIGHTCYAN          ="96"
    BRIGHTWHITE         ="97"

    NOBG                ="m"
    REDBG               =";41m"
    GREENBG             =";42m"
    YELLOWBG            =";43m"
    BLUEBG              =";44m"
    MAGENTABG           =";45m"
    CYANBG              =";46m"
    WHITEBG             =";47m"
    GRAYBG              =";100m"
    GREYBG              =";100m"
    BRIGHTREDBG         =";101m"
    BRIGHTGREENBG       =";102m"
    BRIGHTYELLOWBG      =";103m"
    BRIGHTBLUEBG        =";104m"
    BRIGHTMAGENTABG     =";105m"
    BRIGHTCYANBG        =";106m"
    BRIGHTWHITEBG       =";107m"

class tf_presets:
    def __init__(self, pretty=False):
        if pretty:
            self.warning = f'{tf.BOLD}{tf.WHITE}{tf.YELLOWBG}'
            self.success = f'{tf.BOLD}{tf.WHITE}{tf.GREENBG}'
            self.info = f'{tf.BOLD}{tf.WHITE}{tf.BLUEBG}'
            self.danger = f'{tf.BOLD}{tf.WHITE}{tf.REDBG}'
            self.danger_blink = f'{tf.BLINK}{tf.WHITE}{tf.REDBG}'
            self.balancer = f'{tf.BOLD}{tf.WHITE}{tf.MAGENTABG}'
            self.server = f'{tf.BOLD}{tf.WHITE}{tf.CYANBG}'
            self.argument = f'{tf.NORMAL}{tf.BLUE}{tf.NOBG}'
            self.server_load = f'{tf.NORMAL}{tf.CYAN}{tf.NOBG}'
        else:
            #disable all formatting by using empty strings
            self.warning = ''
            self.success = ''
            self.info = ''
            self.danger = ''
            self.danger_blink = ''
            self.balancer = ''
            self.server = ''
            self.argument = ''
            self.server_load = ''
            
    def header(self, string, preset):
        return f'{preset}{string}{tf.RESET}' if preset else string