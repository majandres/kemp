from tkinter import *
from tkinter import ttk


def msts_to_ip(*args):

    try:
        # create array, [0] contains the IP and [1] contains the port
        msts_cookie = str(msts.get())
        msts_array = msts_cookie.split('.')

        # convert to int -> hex (string) and remove the leading 0x
        msts_hex_ip = str(hex(int(msts_array[0])))[2:]

        # remove two bytes at a time (from left to right), and store in a list
        ip_octets = []
        for x in range(4):
            ip_octets.append(msts_hex_ip[:2])

            # rewrite without the first two characters
            msts_hex_ip = msts_hex_ip[2:]

        # convert the list (ip_octets) from hex to decimal and into a string (i.e. 192.168.0.89)
        ip_addr = ''
        for i in range(3, -1, -1):
            ip_octets[i] = str(int(ip_octets[i], 16))

            if i != 0:
                ip_addr += ip_octets[i] + '.'  # only append the '.' if it's not the last octet
            else:
                ip_addr += ip_octets[i]

        # --------------------------Now lets convert the port value! (if entered)-------------------------- #

        try:
            # convert to int -> hex (string) and remove the leading 0x
            msts_hex_port = str(hex(int(msts_array[1])))[2:]
            
            # it's important that there's an EVEN number of hexadecimals; pre-append 0 if not.
            if msts_hex_port.__len__() % 2 != 0:
                msts_hex_port = "0" + msts_hex_port
            
            # remove two bytes at a time (from left to right), and store in a list
            port = []
            for x in range(2):
                port.append(msts_hex_port[:2])

                # rewrite without the first two characters
                msts_hex_port = msts_hex_port[2:]

            # reverse the bytes and convert into a string that can be converted from hex to decimal
            port_number = ''
            for i in range(1, -1, -1):
                port_number += port[i]

            # convert from hex to decimal (as string)
            port_number = str(int(port_number, 16))

            # set the ip address and port (if entered) in the msts cookie textbox
            ip.set(ip_addr + ':' + port_number)

        except Exception:
            # set the ip address (no port was entered)
            ip.set(ip_addr)

    except ValueError:
        pass

# Used the tutorial from tkinter to build the GUI
# http://www.tkdocs.com/tutorial/firstexample.html
# all comments are from the tutorial

# create a frame widget, which will hold all the content of our user interface, and place that in our main window
root = Tk()
root.title("MSTS to IP")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

msts = StringVar()
ip = StringVar()

msts_entry = ttk.Entry(mainframe, width=18, textvariable=msts)
msts_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=ip).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=msts_to_ip).grid(column=2, row=3, sticky=W)

ttk.Label(mainframe, text="msts cookie").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)

# walks through all of the widgets that are children of our content frame,
# and adds a little bit of padding around each, so they aren't so scrunched together.
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# the cursor will start in that field, so the user doesn't have to click in it before starting to type.
msts_entry.focus()

# if the user presses the Return key (Enter on Windows) anywhere within the root window,
# that it should call our msts_to_ip function, the same as if the user pressed the Calculate button.
root.bind('<Return>', msts_to_ip)

# tells Tk to enter its event loop, which is needed to make everything run.
root.mainloop()
