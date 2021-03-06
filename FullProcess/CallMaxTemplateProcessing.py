import json

from COREDB.MaxTemplatePrivateUpdate import update_private_max_template
from COREDB.MaxTemplatePrivatePull import pull_private_details_raw
from COREDB.MaxTemplatePublicUpdate import update_public_max_template, drop_public_max_template
from COREDB.MaxTemplatePublicPull import get_public_id_from_private_course_manifest, \
    pull_public_details_raw
from FullProcess.MaxScheduleGeneration import generate


def generate_and_update_db_private_template(course_object_list, discord_user_id):
    """
    :param course_object_list:
    :param discord_user_id:
    :return:
    """
    if len(course_object_list) == 0:
        raise ValueError("Missing course values")

    course_raw_str_list = []
    for course in course_object_list:
        course_raw_str_list.append(course.get_raw_str())

    public_id_num = get_public_id_from_private_course_manifest(course_raw_str_list=course_raw_str_list)

    if public_id_num < 0:  # No public match, save this private custom max schedule template
        max_schedules = generate(course_object_list)  # Generate all schedule combos

        if len(max_schedules) > 0:  # Successfully generated a max schedule
            update_private_max_template(max_schedule=max_schedules, discord_user_id=discord_user_id)
        else:    # Failed to generate any possible schedules
            raise RuntimeError("No schedule combos were generated with the given conditions")
    else:
        raise ValueError(f"A public template with the same course manifest exists!\nPlease use id = {public_id_num}")


def pull_private_details_str(discord_id):
    details_list = pull_private_details_raw(discord_id)

    if len(details_list) > 0:
        return_str = (f"User ID: {details_list[0][0]}\n"
                      f"Course Manifest: {', '.join(json.loads(details_list[0][1]))}\n"
                      f"Updated: {details_list[0][2].strftime('%Y/%m/%d %H:%M:%S')}\n\n")
    else:
        return_str = "No Public Template details found"
    return return_str


def generate_and_update_db_public_template(course_object_list, description=None):
    max_schedules = generate(course_object_list)  # Generate all schedule combos

    if len(max_schedules) > 0:  # Successfully generated a max schedule
        update_public_max_template(max_schedule=max_schedules, description=description)
    else:  # Failed to generate any possible schedules
        raise RuntimeError("No schedule combos were generated with the given conditions")


def pull_public_details_str(id_num=None):
    details_list = pull_public_details_raw(id_num)

    return_str = ""
    for detail in details_list:
        return_str += (f"ID: {detail[0]}\n"
                       f"Description: {detail[1]}\n"
                       f"Course Manifest: {', '.join(json.loads(detail[2]))}\n"
                       f"Updated: {detail[3].strftime('%Y/%m/%d %H:%M:%S')}\n\n")

    return_str += "" if len(return_str) > 0 else "No Public Template details found"

    return return_str


def drop_public_templates(id_nums):
    if len(id_nums) == 0:
        raise ValueError("Missing id num values")

    for id_num in id_nums:
        drop_public_max_template(int(id_num))
