import pandas as pd
faroese_countries = ['Andorra','Aserbadjan','Belgia','Bosnia-Hersigovina','Danmark', 'Estland','Eysturríki',
                     'Finnland','Frakland','Grikkaland','Holland','Italia','Írland','Ísland',
                     'Ísrael','Jugoslavia','Kanada','Kasakstan','Kekkia','Kekkoslovakia','Kýpros','Lettland',
                     'Liktinstein','Litava','Luksemborg','Moldova','Norðurírland','Noreg','Pólland',
                     'Rumenia','Russland','Skotland','Spania','Sveis','Svøríki','Turkaland','Týskland','Ukraina',
                     'Ungarn','Føroyar']
english_countries = ['Andora','Azerbaijan','Belgium','Bosnia - Herzegovina','Denmark', 'Estonia','Austria',
                     'Finland','France','Greece','Netherlands','Italy','Ireland','Iceland',
                     'Israel','Yugoslavia','Canada','Kazakhstan','Czech Republic','Czechoslovakia','Cyprus','Latvia',
                     'Liechtenstein','Lithuania','Luxembourg','Moldova','Northern Ireland','Norway','Poland',
                     'Romania','Russia','Scotland','Spain','Switzerland','Sweden','Turkey','Germany','Ukraine',
                     'Hungary', 'Faroe Islands']


def translate_faroese_countries(df):
    for i in range(0, len(faroese_countries)-1):
        df['Opponent'] = df['Opponent'].str.replace(faroese_countries[i], english_countries[i])
    return df