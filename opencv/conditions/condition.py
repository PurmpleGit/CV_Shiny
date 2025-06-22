import cv2
import cv2.typing
from conditions.confidence import Confidence

class Condition:
    raw_sprite: cv2.typing.MatLike
    processed_sprite: cv2.typing.MatLike
    sprite_mask: cv2.typing.MatLike | None
    last_max: tuple[float, float, cv2.typing.Point, cv2.typing.Point] | None
    confidence: Confidence

    def __init__(self, sprite_path:str, confidence:Confidence = Confidence.MEDIUM):
        self.raw_sprite = cv2.resize(cv2.imread(sprite_path, cv2.IMREAD_UNCHANGED), None ,fx=1, fy=1, interpolation = cv2.INTER_NEAREST_EXACT)
        self.processed_sprite = cv2.cvtColor(self.raw_sprite, cv2.IMREAD_COLOR_BGR)
        self.last_result = None
        self.confidence = confidence

        has_alpha_channel = (self.raw_sprite[0][0].size == 4)
        if(has_alpha_channel):
            (void, self.sprite_mask) = cv2.threshold(self.raw_sprite[:, :, 3], 0, 255, cv2.THRESH_BINARY)
        else:
            self.sprite_mask = None

    def draw(self, screen_builder: cv2.typing.MatLike, name: str) ->  cv2.typing.MatLike:
        match_height = self.raw_sprite.shape[0]
        match_width = self.raw_sprite.shape[1]

        (void, match_percentage, void, match_location) = self.last_result
        #Results with masks can have INF or NAN values: https://github.com/opencv/opencv/issues/15768
        scaled_match_percentage = (min((max(match_percentage, 0.95) - 0.95),0.05) * 20)
        box_color:cv2.typing.Scalar = (255, 255, 255)
        screen_bounding_box_text = cv2.putText(screen_builder, f'{scaled_match_percentage*100:.0f}% {name}', match_location, cv2.FONT_HERSHEY_PLAIN, 1.5, box_color, lineType = cv2.LINE_AA)
        cv2.addWeighted(screen_bounding_box_text[match_location[1]:match_location[1]+match_height,match_location[0]:match_location[0]+match_width],0.5,self.processed_sprite,0.5,0,screen_bounding_box_text[match_location[1]:match_location[1]+match_height,match_location[0]:match_location[0]+match_width])
        return screen_bounding_box_text
    
    def checkPoint(self, raw_screen: cv2.typing.MatLike, check_location:cv2.typing.Point) ->  cv2.typing.MatLike:
        result = cv2.matchTemplate(cv2.cvtColor(raw_screen, cv2.IMREAD_COLOR_BGR), self.processed_sprite, cv2.TM_CCORR_NORMED, None, self.sprite_mask)
        self.last_result = (None, result[check_location[1]][check_location[0]], None, check_location)

    def isMet(self, raw_screen: cv2.typing.MatLike) -> bool:
        result = cv2.matchTemplate(cv2.cvtColor(raw_screen, cv2.IMREAD_COLOR_BGR), self.processed_sprite, cv2.TM_CCORR_NORMED, None, self.sprite_mask)
        self.last_result = cv2.minMaxLoc(result)
        #Results with masks can have INF or NAN values: https://github.com/opencv/opencv/issues/15768
        return (self.last_result[1] <= 1 and self.last_result[1] > self.confidence.value)