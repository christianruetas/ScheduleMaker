from PIL import Image, ImageDraw, ImageFont


COLUMN_SIZE = 200
ROW_SIZE = 80
HEADER_FONT = ImageFont.truetype('roboto-mono/RobotoMono-Bold.ttf', 32)
BODY_FONT = ImageFont.truetype('roboto-mono/RobotoMono-Medium.ttf', 20)
WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

BLUE = (157, 162, 233)
MOSS = (171, 210, 172)
UBE = (208, 178, 241)
COLOUR_MIX = [BLUE, MOSS, UBE]


def draw_schedule(schedule_obj):
    """
    draws a .png image of a TermSchedule object
    :param schedule_obj:
    """
    global COLUMN_SIZE, ROW_SIZE, HEADER_FONT, WEEKDAYS, COLOUR_MIX

    if not isinstance(schedule_obj, TermSchedule):
        raise TypeError

    img = Image.new("RGB", (COLUMN_SIZE * 8, ROW_SIZE * 14), color="white")
    d = ImageDraw.Draw(img)

    for col_i in range(1, 8):
        text = WEEKDAYS[col_i - 1]
        d.text((COLUMN_SIZE * col_i, 10), text, font=HEADER_FONT, fill="black", align="left")

    for row_i in range(8, 21):
        text = str(row_i) + ":00"
        text = " " + text if len(text) < 5 else text
        d.text((10, ROW_SIZE * (row_i - 7)), text, font=HEADER_FONT, fill="black", align="left")
        # time off set >>>>>>>>>>>>>>>>>^ start at 8:00

    if TermSchedule.is_valid:
        colour_counter = 0
        for class_obj in schedule_obj.classes:
            __draw_class(img=img, class_obj=class_obj, block_colour=COLOUR_MIX[colour_counter % len(COLOUR_MIX)])
            colour_counter += 1

    img.save('schedule.png')


def __draw_class(img, class_obj, block_colour):
    global COLUMN_SIZE, ROW_SIZE, BODY_FONT

    d = ImageDraw.Draw(img)

    if class_obj.class_time is None:
        return

    for class_time in class_obj.class_time:
        if class_time is not None:
            x_1_cord = COLUMN_SIZE * (class_time[0].weekday() + 1)
            x_2_cord = COLUMN_SIZE * (class_time[0].weekday() + 2)
            y_1_cord = (((class_time[0].hour - 8) + class_time[0].minute / 60) + 1) * ROW_SIZE
            y_2_cord = (((class_time[1].hour - 8) + class_time[1].minute / 60) + 1) * ROW_SIZE

            d.rectangle((x_1_cord, y_1_cord, x_2_cord, y_2_cord), fill=block_colour, outline="black", width=3)

            text = str(class_obj.fac)[:7] + " " + str(class_obj.uid)[:7]
            d.text((x_1_cord + 10, y_1_cord + 5), text, font=BODY_FONT, fill="black")
            text = str(class_obj.crn)[:15]
            d.text((x_1_cord + 10, y_1_cord + 5 + BODY_FONT.size), text, font=BODY_FONT, fill="black")
            text = str(class_obj.title)[:15 - 4] + " " + str(class_obj.class_type)[:3]
            d.text((x_1_cord + 10, y_1_cord + 5 + (BODY_FONT.size * 2)), text, font=BODY_FONT, fill="black")


# TODO TEST CODE
from ClassStructure.CourseClassStructure import AClass
from ClassStructure.SingleScheduleStructure import TermSchedule
from datetime import datetime

time = [[datetime(2021, 7, 10, 8), datetime(2021, 7, 10, 10)], [datetime(2021, 7, 11, 8), datetime(2021, 7, 11, 9)]]
passer = TermSchedule([AClass(fac="FAC", uid="1000U", title="YOINK CLASS", class_time=time, crn=1234, class_type="Laboritory")])

draw_schedule(passer)