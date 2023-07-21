import utils


class Colorize:
    def __init__(self):
        config = utils.read_config('config.ini')
        color_map = config['color']
        self.color_map = color_map
        self.name2code = {
            'BLACK': 30,
            'RED': 31,
            'GREEN': 32,
            'YELLOW': 33,
            'BLUE': 34,
            'PURPLE': 35,
            'CYAN': 36,
            'GREY': 37,
            'WHITE': 38,

            'BLACK-GROUND': 40,
            'RED-GROUND': 41,
            'GREEN-GROUND': 42,
            'YELLOW-GROUND': 43,
            'BLUE-GROUND': 44,
            'PURPLE-GROUND': 45,
            'CYAN-GROUND': 46,
            'GREY-GROUND': 47,
        }

    def colorize_text(self, text, attr):

        if attr in self.color_map.keys():
            color_name = self.color_map[attr]
        else:
            color_name = 'WHITE'
        color_code = self.name2code[color_name]
        return f"\033[{color_code}m{text}\033[0m"

    def colorize_list(self, list_data):
        for m_data in list_data:
            for k in m_data.keys():
                r = self.colorize_text(m_data[k], k)
                m_data[k] = r