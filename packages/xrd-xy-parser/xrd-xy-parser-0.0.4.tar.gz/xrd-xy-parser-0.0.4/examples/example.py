from xrd_xy_parser import xy

if __name__ == "__main__":

    try:
        header, body, footer = xy.readstr("examples/example.xy")
        print("header:{}\n" "body:{}\n" "footer:{}\n".format(header, body, footer))

    except xy.ParseError as e:
        print(e)
