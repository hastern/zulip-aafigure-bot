import re
import tempfile
import logging

import aafigure

from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AAFigureBotHandler:
    """
    This plugin converts ASCII art into SVGs
    """

    META = {
        "name": "aafigure",
        "description": "Render any message using FIGlet. Power by pyfiglet.",
    }

    def usage(self) -> str:
        return """
            This plugin allows a user to render an ascii-art drawing using aafigure
            """

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
        quoted_name = bot_handler.identity().mention
        content = message["content"].strip()

        try:
            if content in ["help", "doc"]:
                bot_handler.send_reply(
                    message,
                    "The aafigure documentation can be found here: [https://aafigure.readthedocs.io/en/latest/shortintro.html](https://aafigure.readthedocs.io/en/latest/shortintro.html)",
                )
            else:
                _, drawing, *_ = content.split("```", 2)

                img = tempfile.TemporaryFile(prefix="aafigure-", suffix=".svg")
                aafigure.aafigure.render(drawing, img, options={"format": "svg"})
                result = bot_handler.upload_file(img)
                logger.debug(result)
                if result["result"] == "success":
                    response = "[]({})".format(result["uri"])
                    bot_handler.send_reply(message, response)
                else:
                    bot_handler.send_reply(
                        message, "Sorry, I failed to upload the image"
                    )
        except aafigure.UnsupportedFormatError as err:
            pass
        except ValueError:
            bot_handler.send_reply(
                message, "Sorry, I couldn't find drawing instructions"
            )
        except Exception as err:
            logger.exception(err)
            bot_handler.send_reply(
                message, "Sorry, I didn't prepare for unforseen consequences"
            )


handler_class = AAFigureBotHandler
