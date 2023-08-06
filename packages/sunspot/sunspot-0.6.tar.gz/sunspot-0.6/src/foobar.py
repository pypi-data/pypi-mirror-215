import sunspot

e = sunspot.Ephemeris(  '2023-6-18 19:26:00',
                        '2023-6-18 19:28:00',
                        '-71.332597,42.458790,0.041',
                        '1 minute',
                        '10',
                        '4,2')


def on_time( args: list ):
    print( "ON-TIME!" )
    for i in range( len(args)-1 ):
        print( args[i] )
    print( "\n" )


def before( args: list ):
    print( "BEFORE!" )
    for i in range( len(args)-1 ):
        print( args[i] )
    print( "\n" )
    import time
    time.sleep(100)


def after( args: list ):
    print( "AFTER!" )
    for i in range( len(args)-1 ):
        print( args[i] )
    print( "\n" )


t = sunspot.Tracker( e, track_before_method=before, track_on_time_method=on_time, track_after_method=after, verbose=True )

# import time
# time.sleep( 60 )
# t.terminate_tracking()


