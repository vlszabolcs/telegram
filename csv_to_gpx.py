
import csv
import json
import calendar,time
import pandas as pd

altimet_csv="sim7000g/202276_16133.csv"

alti_tim="dTime"
alti_lat="Latitude"
alti_lon="Longitude"
alti_gpsalti="MSL Altitude"
alti_spd="Speed"
alti_lcp="pressure"
alti_tem="temperature"
alti_alt="altitude"

def dic_to_list(dic):
    my_list=[]
    for var in dic:
        my_list.append(var)
    
    return my_list

def csv_to_dic(filename):
    dic=[] 
    with open(filename, 'r') as data:  
        for line in csv.DictReader(data):
            dic.append(line)
    return dic

def time_wizard(old_list):
    newList=[]

    for x in old_list:  
        time_in=x.get(alti_tim)

        
        time_in=time_in.replace(".","")
        day=time_in[6:8]
        month=time_in[4:6]
        year=time_in[0:4]

        hour=time_in[8:10]
        min=time_in[10:12]
        sec=time_in[12:14]
        milsec=time_in[15:19]


        new_time=year+"-"+month+"-"+day+" "+hour+":"+min+":"+sec+"."+milsec
        new_time=calendar.timegm(time.strptime(new_time, '%Y-%m-%d %H:%M:%S.%f'))
        """
        new_time=time_in
        new_time=calendar.timegm(time.strptime(new_time, '%Y%m%d%H%M%S'))
        print(new_time)
        """
        x[alti_tim]=new_time
        newList.append(x)

    return newList

def dataframe_to_gpx(input_df, output_file,alts_colname):
        """
        convert pandas dataframe to gpx
        input_df: pandas dataframe
        lats_colname: name of the latitudes column
        longs_colname: name of the longitudes column
        times_colname: name of the time column
        alts_colname: name of the altitudes column
        output_file: path of the output file
        """
        import gpxpy.gpx
        gpx = gpxpy.gpx.GPX()


        lats_colname=alti_lat,
        longs_colname=alti_lon,
        times_colname=alti_tim

        json_df = []
        json_df=pd.read_json(input_df)
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        for idx in json_df.index:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(json_df.loc[idx, lats_colname],
                                                              json_df.loc[idx, longs_colname],
                                                              time=pd.to_datetime(json_df.loc[idx, times_colname],unit='s') if times_colname else None,
                                                              elevation=json_df.loc[idx, alts_colname] if alts_colname else None))
        
        with open(output_file, 'w') as f:
            f.write(gpx.to_xml())
        return gpx.to_xml()

def csv_to_gpx_original(input_cs):
    alti_data=time_wizard(csv_to_dic(input_cs))
    input_cs=input_cs.replace("csv","gpx")
    input_cs="orig_"+input_cs
    print(input_cs)
    originalAlti=dataframe_to_gpx(json.dumps(alti_data),input_cs,alti_gpsalti)
    return input_cs

def csv_to_gpx_alti(input_cs):
    alti_data=time_wizard(csv_to_dic(input_cs))
    input_cs=input_cs.replace("csv","gpx")
    input_cs="pres_"+input_cs
    print(input_cs)
    originalAlti=dataframe_to_gpx(json.dumps(alti_data),input_cs,alti_alt)
    return input_cs