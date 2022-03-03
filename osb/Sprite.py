from xmlrpc.client import boolean


try:
    import re
except:
    raise ImportError("Please make sure all libraries are installed")


class Sprite():
    def __init__(self, filepath, layer="Background", origin="TopLeft", pos=(0, 0)):
        self.filepath = filepath
        self.layer = layer
        self.origin = origin
        self.pos = pos
        self.commands = []

    def _convert_time(self, time):
        '''08:38:685
        \d{2}:\d{2}:\d{3}'''
        if type(time) == int:
            return time
        elif type(time) == str:
            time = re.search(r'\d{2}:\d{2}:\d{3}', time)
            if time:
                return sum([int(t) * 60000 if i == 0 else int(t) * 1000 if i == 1 else int(t)
                            for i, t in enumerate(time.group().split(":"))])
            else:
                raise ValueError(
                    "Could not find correct time in provided value. Please make sure time is 00:00:000 format.")
        else:
            raise TypeError("Could not find time string in given time")

    def _check_easing(self, easing):
        try:
            easing = int(easing)
        except:
            pass
        if type(easing) != int:
            raise TypeError
        elif easing not in range(35):
            raise ValueError("Easing must be between 0 and 34")
        else:
            return easing

    def _check_loop_trigger(self, loop_trigger):
        if type(loop_trigger) != bool:
            raise TypeError("loop_trigger is not True or False")
        else:
            return "__" if loop_trigger else "_"

    def fade(self, start_time, end_time, start_opacity, end_opacity, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_opacity) not in [float, int]:
            raise TypeError("start_opacity is not a float or int")
        elif start_opacity > 1 or start_opacity < 0:
            raise ValueError(
                f"start_opacity value of {start_opacity} is not between 0 and 1")
        if type(end_opacity) not in [float, int]:
            raise TypeError("end_opacity is not a float or int")
        elif end_opacity > 1 or end_opacity < 0:
            raise ValueError(
                f"end_opacity value of {end_opacity} is not between 0 and 1")
        easing = self._check_easing(easing)
        self.commands.append(
            f'{loop_trigger}F,{easing},{start_time},{end_time},{start_opacity},{end_opacity}')

    def move(self, start_time, end_time, start_cords, end_cords, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_cords) not in [list, tuple]:
            raise TypeError("start_cords is not a valid tuple of values")
        elif len(start_cords) != 2:
            raise ValueError(
                "The are to many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in start_cords]):
            raise TypeError("Tuple does not contain integers")
        if type(end_cords) not in [list, tuple]:
            raise TypeError("end_cords is not a valid tuple of values")
        elif len(end_cords) != 2:
            raise ValueError(
                "The are to many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in end_cords]):
            raise TypeError("Tuple does not contain integers")
        self.commands.append(
            f'{loop_trigger}M,{easing},{start_time},{end_time},{start_cords[0]},{start_cords[1]},{end_cords[0]},{end_cords[1]}')

    def moveX(self, start_time, end_time, start_cord, end_cord, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_cord) != int:
            raise TypeError("Start_cord is not an integer")
        if type(end_cord) != int:
            raise TypeError("End_cord is not an integer")
        self.commands.append(
            f'{loop_trigger}MX,{easing},{start_time},{end_time},{start_cord},{end_cord}')

    def moveY(self, start_time, end_time, start_cord, end_cord, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_cord) != int:
            raise TypeError("Start_cord is not an integer")
        if type(end_cord) != int:
            raise TypeError("End_cord is not an integer")
        self.commands.append(
            f'{loop_trigger}MY,{easing},{start_time},{end_time},{start_cord},{end_cord}')

    def scale(self, start_time, end_time, start_scale, end_scale, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_scale) not in [float, int]:
            raise TypeError("start_scale is not a float or int")
        elif start_scale < 0:
            raise ValueError(
                f"start_scale value of {start_scale} can not be less than 0")
        if type(end_scale) not in [float, int]:
            raise TypeError("end_scale is not a float or int")
        elif end_scale < 0:
            raise ValueError(
                f"end_scale value of {end_scale} can not be less than 0")
        self.commands.append(
            f'{loop_trigger}S,{easing},{start_time},{end_time},{start_scale},{end_scale}')

    def vecscale(self, start_time, end_time, start_scales, end_scales, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_scales) not in [list, tuple]:
            raise TypeError("start_scales is not a valid tuple of values")
        elif len(start_scales) != 2:
            raise ValueError(
                "The are to many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in start_scales]) and not all([c > 0 for c in start_scales]):
            raise TypeError(
                "Tuple does not contain integers that are greater than 0")
        if type(end_scales) not in [list, tuple]:
            raise TypeError("end_scales is not a valid tuple of values")
        elif len(end_scales) != 2:
            raise ValueError(
                "The are to many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in end_scales]) and not all([c > 0 for c in end_scales]):
            raise TypeError(
                "Tuple does not contain integers that are greater than 0")
        self.commands.append(
            f'{loop_trigger}M,{easing},{start_time},{end_time},{start_scales[0]},{start_scales[1]},{end_scales[0]},{end_scales[1]}')

    def rotate(self, start_time, end_time, start_rotate, end_rotate, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_rotate) not in [float, int]:
            raise TypeError("start_rotate is not a float or int")
        if type(end_rotate) not in [float, int]:
            raise TypeError("end_rotate is not a float or int")
        self.commands.append(
            f'{loop_trigger}F,{easing},{start_time},{end_time},{start_rotate},{end_rotate}')

    def colour(self, start_time, end_time, start_colour, end_colour, easing=0, loop_trigger=False):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        loop_trigger = self._check_loop_trigger(loop_trigger)
        if type(start_colour) not in [list, tuple]:
            raise TypeError("start_colour is not a valid tuple of values")
        elif len(start_colour) != 3:
            raise ValueError(
                "The are too many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in start_colour]) and not all([(c > 0) and (c < 255) for c in start_colour]):
            raise TypeError(
                "Tuple does not contain integers that are greater are correct colour parameter")
        if type(end_colour) not in [list, tuple]:
            raise TypeError("end_colour is not a valid tuple of values")
        elif len(end_colour) != 3:
            raise ValueError(
                "The are too many or not enough points in the provided tuple")
        elif not all([type(c) == int for c in end_colour]) and not all([(c > 0) and (c < 255) for c in end_colour]):
            raise TypeError(
                "Tuple does not contain integers that are greater are correct colour parameter")
        self.commands.append(
            f'{loop_trigger}M,{easing},{start_time},{end_time},{start_colour[0]},{start_colour[1]},{start_colour[2]},{end_colour[0]},{end_colour[1]},{end_colour[2]}')

    def color(self, start_time, end_time, start_color, end_color, easing=0, loop_trigger=False):
        self.colour(start_time, end_time, start_color,
                    end_color, easing, loop_trigger)

    def loop(self, start_time, loop_count):
        start_time = self._convert_time(start_time)
        if type(loop_count) != int:
            raise TypeError("loop_count must be an integer")
        elif loop_count > 0:
            raise ValueError("Can not have a loop less than 0")
        else:
            self.commands.append(f"_L,{start_time},{loop_count}")

    def flip_horizontal(self, start_time, end_time, easing=0):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        self.commands.append(f"_P,{easing},{start_time},{end_time},H")

    def flip_vertically(self, start_time, end_time, easing=0):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        self.commands.append(f"_P,{easing},{start_time},{end_time},V")

    def additive_colour(self, start_time, end_time, easing=0):
        start_time = self._convert_time(start_time)
        end_time = self._convert_time(end_time)
        easing = self._check_easing(easing)
        self.commands.append(f"_P,{easing},{start_time},{end_time},A")
