import discord
from discord.ext import commands

from constants import SCHEDULE_PNG_FILENAME, RESULT_TXT_FILENAME
from FullProcess.CallPngAndTextGenerate import generate_png_and_txt
from FullProcess.CallDirectScheduleFromCRNs import generate_term_schedule_from_crn_list


class DirectCRNScheduleCog(commands.Cog):

    @commands.command(aliases=["display"])
    async def display_from_crn(self, ctx, *crn_codes):
        try:
            single_term_schedule = generate_term_schedule_from_crn_list(crn_codes)

            # Check for possible bad crn codes
            if len(single_term_schedule.classes) != len(crn_codes):
                await ctx.reply("Warning! Some CRN codes specified could not be found", mention_author=False)

            # Generate Result text
            found_crn_code_matches = []
            for class_object in single_term_schedule.classes:
                found_crn_code_matches.append(str(class_object.crn))  # Cast as str to ensure .join works

            crn_codes_str = ", ".join(found_crn_code_matches)  # Join as a string
            result_txt = f"Display Source CRNs =\n{crn_codes_str}\n"

            # Generate a png and txt
            generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)

            # Discord send schedule.png
            with open(f"DiscordBotStuff/PNGMaker/{SCHEDULE_PNG_FILENAME}", "rb") as png_file:
                await ctx.message.author.send(file=discord.File(png_file, SCHEDULE_PNG_FILENAME))

            # Discord send results.txt
            with open(f"DiscordBotStuff/{RESULT_TXT_FILENAME}", "rb") as file:
                await ctx.message.author.send(file=discord.File(file, RESULT_TXT_FILENAME))

        except ValueError as e:
            await ctx.reply(f"ValueError -> {e}", mention_author=False)
        except TypeError as e:
            await ctx.reply(f"TypeError -> {e}", mention_author=False)
        except RuntimeError as e:
            await ctx.reply(f"RuntimeError -> {e}", mention_author=False)
        except Exception as e:
            raise e


def setup(client):
    client.add_cog(DirectCRNScheduleCog(client))