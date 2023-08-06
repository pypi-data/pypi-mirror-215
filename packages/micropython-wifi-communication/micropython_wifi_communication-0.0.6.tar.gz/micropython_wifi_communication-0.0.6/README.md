# comu

server

init

    from comu.ser import se
    
    s = se(net=True)
    #se(net={'SSID':...,'PASSWORD':....})

recv
    
    from time import sleep
    
    while True:
        data = s.recv()
        if data:
            print(data)
        sleep(1)

send

    from time import sleep
    
    x = 0

    while True:
        s.send(x)
        x+=1
        sleep(1)


client

    from comu.cli import ci
    
    c = ci(net=True)
    #ci(net={'ssid':...,'password':....}) or ci()

recv
    
    from time import sleep
    
    while True:
        data = c.recv()
        if data:
            print(data)
        sleep(1)

send

    from time import sleep
    
    x = 0

    while True:
        c.send(x)
        x+=1
        sleep(1)