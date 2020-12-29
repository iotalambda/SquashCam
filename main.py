from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
import kivy.properties as kv_props
from random import randint
from kivy.core.window import Window
from kivy.event import EventDispatcher


class SideHitDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type("on_side_hit")
        super(SideHitDispatcher, self).__init__(**kwargs)

    def on_side_hit(self, isLeft):
        pass


class PongBall(Widget):
    velocity_x = kv_props.NumericProperty(0)
    velocity_y = kv_props.NumericProperty(0)

    velocity = kv_props.ReferenceListProperty(velocity_x, velocity_y)

    def update(self, side_hit_dispatcher):
        self.pos = Vector(*self.velocity) + self.pos

        if self.x < 0:
            self._hit_left_wall(side_hit_dispatcher)
        elif self.x > self.parent.width - self.width:
            self._hit_right_wall(side_hit_dispatcher)

        if (self.y < 0) or (self.y > self.parent.height - self.height):
            self._turn_around_y()

    def hit_player(self):
        self._turn_around_x()

    def _hit_left_wall(self, side_hit_dispatcher):
        side_hit_dispatcher.dispatch("on_side_hit", True)
        self._turn_around_x()

    def _hit_right_wall(self, side_hit_dispatcher):
        side_hit_dispatcher.dispatch("on_side_hit", False)
        self._turn_around_x()

    def _turn_around_x(self):
        self.velocity_x *= -1

    def _turn_around_y(self):
        self.velocity_y *= -1


class PongPaddle(Widget):
    velocity_y = kv_props.NumericProperty(0)
    score = kv_props.NumericProperty(0)

    def __init__(self, **kwargs):
        super(PongPaddle, self).__init__(**kwargs)

    def update(self, ball):
        self._check_ball(ball)
        if self._check_oob(self.velocity_y > 0):
            return
        self.pos = Vector(0, self.velocity_y) + self.pos

    def try_go_up(self):
        self.velocity_y = 10

    def try_go_down(self):
        self.velocity_y = -10

    def stop(self):
        self.velocity_y = 0

    def score_point(self):
        self.score += 1

    def _check_oob(self, tries_go_up):
        if (not tries_go_up and self.y < 0) or (
            tries_go_up and self.y > self.parent.height - self.height
        ):
            self.stop()
            return True
        return False

    def _check_ball(self, ball):
        if self.collide_widget(ball):
            ball.hit_player()


class PongGame(Widget):

    ball = kv_props.ObjectProperty()
    player_left = kv_props.ObjectProperty()
    player_right = kv_props.ObjectProperty()
    _keys_pressed = {"w": False, "s": False, "o": False, "l": False}

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self._side_hit_dispatcher = SideHitDispatcher()
        self._side_hit_dispatcher.bind(on_side_hit=self._on_side_hit)

    def update(self, dt):
        self.ball.update(self._side_hit_dispatcher)
        self.player_left.update(self.ball)
        self.player_right.update(self.ball)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _update_key_based_movements(self):
        if self._keys_pressed["w"]:
            self.player_left.try_go_up()
        elif self._keys_pressed["s"]:
            self.player_left.try_go_down()
        else:
            self.player_left.stop()

        if self._keys_pressed["o"]:
            self.player_right.try_go_up()
        elif self._keys_pressed["l"]:
            self.player_right.try_go_down()
        else:
            self.player_right.stop()

    def _on_key_down(self, keyboard, keycode, *_):
        if keycode[1] in self._keys_pressed.keys():
            self._keys_pressed[keycode[1]] = True
        self._update_key_based_movements()

    def _on_key_up(self, keyboard, keycode, *_):
        if keycode[1] in self._keys_pressed.keys():
            self._keys_pressed[keycode[1]] = False
        self._update_key_based_movements()

    def _on_side_hit(self, *args):
        if args[1] is True:
            self.player_right.score_point()
        else:
            self.player_left.score_point()


class SquashCamApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    SquashCamApp().run()
