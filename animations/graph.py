from manim import *
import numpy

GRAPH_WIDTH=20000
GRAPH_WIDTH_RALTZ=400000
GRAPH_HEGHT=1
ORIGIN_BOTTOM_LEFT = numpy.array((0, 0, 0));

config.pixel_width = 1800
config.pixel_height = 1800

class SquareToCircle(Scene):

    @staticmethod
    def captureProbability(x):
        return 1 - pow((8191/8192),x)
    
    @staticmethod
    def captureProbabilityRaltz(x):
        return 1 - pow((204799/204800),x)

    @staticmethod
    def makePoint(label:str, x_position:str, y_position:str, axis:Axes, color:ManimColor) -> VGroup:
        point = VGroup()
        point += Dot(point= axis@(x_position, y_position, 0), color=color)
        point += axis.get_horizontal_line(axis@(x_position, y_position, 0), color=color)
        point += axis.get_vertical_line(axis@(x_position, y_position, 0), color=color)
        point += Tex(label, color=color).scale(1).next_to(axis @ (x_position, y_position, 0))
        return point
    
    def construct(self):
        axis = Axes(
                    x_range =[0, GRAPH_WIDTH, GRAPH_WIDTH/4],
                    y_range =[0,GRAPH_HEGHT, GRAPH_HEGHT/10], 
                    x_length=10, 
                    y_length=10, 
                    axis_config={
                         "include_numbers":
                         True},
                    tips=False
                    );
        
        #
        y_axis_label =  axis.get_y_axis_label("Chance\ of\ At\ Least\ 1\ Shiny", edge=LEFT).rotate(PI/2).move_to(axis@(0 - (GRAPH_WIDTH/10), GRAPH_HEGHT/2, 0))
        x_axis_label =  axis.get_x_axis_label("Number\ of\ Encounters", edge=DOWN).move_to(axis@((GRAPH_WIDTH/2), 0 -(GRAPH_HEGHT/10), 0))
        axis_labels = VGroup(x_axis_label, y_axis_label)

        
        #
        plot = axis.plot(SquareToCircle.captureProbability, color=PURPLE)
        #

        formula = Tex("\\begin{equation*}P(x) = 1 - (\\frac{8191}{8192})^x \\end{equation*}", color=PURPLE).scale(2).next_to(axis @(GRAPH_WIDTH * 0.1, GRAPH_HEGHT* 0.5, 0))
        formula_moved = Tex("\\begin{equation*}P(x) = 1 - (\\frac{8191}{8192})^x \\end{equation*}", color=PURPLE).scale(1).next_to(axis @(GRAPH_WIDTH * 0.43, GRAPH_HEGHT* 0.4, 0))

        formula_expected_time = Tex("\\begin{equation*} (\\frac{(\\frac{18862\ Encounters}{5\ Encounters\ per\ Minute})}{60\ Minutes\ per\ Hour}) = 62.87 \ Hours!\\end{equation*}", color=PURPLE).scale(1.2).next_to(axis @(GRAPH_WIDTH * -0.1, GRAPH_HEGHT* 0.5, 0))
        

        point_50 = SquareToCircle.makePoint("50\% @ 5,678", 5678, 0.5, axis, RED)
        point_63 = SquareToCircle.makePoint("63\% @ 8,192", 8192, 0.6321, axis, BLUE)
        point_90 = SquareToCircle.makePoint(" \\\\90\% \\\\@\\\\ 18,862", 18862, 0.9, axis, GREEN)




        axis_raltz = Axes(
                    x_range =[0, GRAPH_WIDTH_RALTZ, GRAPH_WIDTH_RALTZ/4],
                    y_range =[0,GRAPH_HEGHT, GRAPH_HEGHT/10], 
                    x_length=10, 
                    y_length=10, 
                    axis_config={
                         "include_numbers":
                         True},
                    tips=False
                    );
        
        y_axis_label_raltz =  axis.get_y_axis_label("Chance\ of\ At\ Least\ 1\ Shiny\ Raltz", edge=LEFT).rotate(PI/2).move_to(axis_raltz@(0 - (GRAPH_WIDTH_RALTZ/10), GRAPH_HEGHT/2, 0))
        x_axis_label_raltz =  axis.get_x_axis_label("Number\ of\ Encounters\ on\ Route\ 102", edge=DOWN).move_to(axis_raltz@((GRAPH_WIDTH_RALTZ/2), 0 -(GRAPH_HEGHT/10), 0))
        axis_labels_raltz = VGroup(y_axis_label_raltz, x_axis_label_raltz)

        formula_raltz = Tex("\\begin{equation*}P(x) = 1 - (1 - (\\frac{1}{8192} \\times \\frac{4}{100}))^x \\end{equation*}", color=PURPLE).scale(1.63).next_to(axis @(GRAPH_WIDTH * (0 - 0.1), GRAPH_HEGHT* 0.5, 0))
        formula_raltz_adjusted = Tex("\\begin{equation*}P(x) = 1 - (1 - (\\frac{1}{8192} \\times \\frac{4}{100}))^x \\end{equation*}", color=PURPLE).scale(0.8).next_to(axis @(GRAPH_WIDTH * (0.1), GRAPH_HEGHT* 0.8, 0))
        plot_raltz = axis_raltz.plot(SquareToCircle.captureProbabilityRaltz, color=PURPLE)

        point_50_raltz = SquareToCircle.makePoint("50\% @ 141,196", 141196, 0.5, axis_raltz, RED)

        formula_expected_time_raltz = Tex("\\begin{equation*} (\\frac{(\\frac{147,196\ Encounters}{5\ Encounters\ per\ Minute})}{60\ Minutes\ per\ Hour}) = 470 \ Hours!\\end{equation*}", color=PURPLE).scale(1.2).next_to(axis @(GRAPH_WIDTH * -0.1, GRAPH_HEGHT* 0.5, 0))


        self.play(Create(axis), Create(axis_labels))
        self.pause(1)
        self.play(Create(formula))
        self.pause(1)
        self.play(Transform(formula, formula_moved), Create(plot))
        self.pause(1)
        self.play(Create(point_50))
        self.pause(1)
        self.play(Transform(point_50, point_63))
        self.pause(1)
        self.play(Transform(point_50, point_90))
        self.pause(1)
        self.play(FadeOut(axis), FadeOut(axis_labels), FadeOut(plot), FadeOut(point_50), Transform(formula, formula_expected_time))
        self.pause(1)
        self.play(Transform(formula, formula_raltz))
        self.pause(1)
        self.play(Create(axis_labels_raltz), Create(axis_raltz), Create(plot_raltz), Transform(formula, formula_raltz_adjusted))
        self.pause(1)
        self.play(Create(point_50_raltz))
        self.pause(1)
        self.play(FadeOut(axis_labels_raltz),FadeOut(axis_raltz),FadeOut(plot_raltz),FadeOut(point_50_raltz),Transform(formula, formula_expected_time_raltz))
        self.pause(3)