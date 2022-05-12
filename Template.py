def render_loop(template, data):
    if "loop_data" in data:

        loop_start_tag = "{{loop}}"
        loop_end_tag = "{{end_loop}}"

        start_index = template.find(loop_start_tag)
        end_index = template.find(loop_end_tag)
        loop_template = template[start_index + len(loop_start_tag) : end_index]
        loop_data = data["loop_data"]
        loop_content = ""
        for i in loop_data:
            loop_content += replace_placeholders(loop_template, i)

        final_content = (
            template[:start_index]
            + loop_content
            + template[end_index + len(loop_end_tag) :]
        )

        return final_content
    else:
        print("ELSE")


def replace_placeholders(template, data):
    replaced_template = template
    for placeholder in data.keys():
        if isinstance(data[placeholder], str):
            toReplace = data[placeholder]
            if placeholder == "filename":
                s = 'src="' + data[placeholder] + '"' + ' alt=""'
                fileContents = open(data[placeholder], "rb")
                picBytes = fileContents.read()
                print(len(picBytes))

                replaced_template = replaced_template.replace(
                    "{{" + placeholder + "}}", s
                )
            else:
                replaced_template = replaced_template.replace(
                    "{{" + placeholder + "}}", data[placeholder]
                )
            # print(toReplace, flush=True)

    return replaced_template
