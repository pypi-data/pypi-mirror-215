import importlib, yaml, pkg_resources, os, warnings, re, requests
import torch 
import bpyth as bpy
import pandas as pd
import pandasklar as pak

    
#############################################################################################################
###
### Helper for Ludwig
###
#############################################################################################################    


def gpu_info():
    # GPU und CUDA
    if torch.cuda.is_available():
        print('CUDA is available on ' + torch.cuda.get_device_name(torch.cuda.current_device()))
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.cuda.empty_cache() # Cache leeren
        print('max_memory_allocated: {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_allocated(device=device)) )  )
        print('max_memory_reserved:  {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_reserved( device=device)) )  )  

    else:
        print('no CUDA!')    



#def entwirre_test_stat(test_stats):
#    result = []
#    for config_no, test_stat in enumerate(test_stats):
#        print(config_no)
#        for output_feature_name, stat in test_stat.items():
#            if output_feature_name == 'combined':
#                continue
#            for key, value in stat.items():
#                if isinstance(value, (int, float)):
#                    result += [[config_no, key, bpy.human_readable_number(value,3) ]]    
#                    
#    result = pak.dataframe(result)
#    result.columns = ['config_no','name','value']
#    return result
#


def analyse_test_stat(run, model_name, test_stat):
    result = []
    for output_feature_name, stat in test_stat.items():
        if output_feature_name == 'combined':
            continue
        for key, value in stat.items():
            if isinstance(value, (int, float)):
                result += [[run, model_name, key, bpy.human_readable_number(value,3) ]]    
                    
    result = pak.dataframe(result)
    result.columns = ['run','model_name','name','value']
    return result









def load_dataset(dataset_name, verbose=True):
    '''
    Loads a dataset from Ludwig's dataset zoo. 
    * dataset_name: Name of the dataset. Valid names are listed by list_datasets().
    Returns a DataFrame with training data and a ludwig.dataset_loader.
    '''
    module         = importlib.import_module('ludwig.datasets')
    dataset_loader = getattr(module, dataset_name)
    data_df       = dataset_loader.load(split=False)
        
    #katalog = list_datasets()
    #mask = katalog.dataset_name == dataset_name
    #katalogeintrag = katalog[mask].iloc[0]

    # nacharbeiten
    if dataset_name == 'agnews':
        dataset_loader.config.output_features = [{'name': 'class', 'type': 'category'}]
        data_df = pak.drop_cols( data_df,'class_index' )
    
    output_feature_names = [col['name'] for col in dataset_loader.config.output_features]   
    data_df = pak.move_cols(data_df, output_feature_names)     
    data_df = pak.move_cols(data_df, 'split',-1) 
    data_df = pak.drop_cols(data_df,['Unnamed: 0','Unnamed: 1'])
    data_df = pak.change_datatype(data_df)

    if verbose:
        print()
        print(dataset_loader.description())    
        print('output_features:', dataset_loader.config.output_features)  
        
    return data_df, dataset_loader



def analyse_cols(data_df, dataset_loader=None, output_features_size=1):
    '''
    Analyses training data. 
    The information whether a column is input_feature or output_feature comes either from
    * dataset_loader (provided by load_dataset), or from
    * output_features_size (then it is the first n columns of the DataFrame).
    If a dataset_loader is provided, output_features_type is taken from config. Otherwise it's guessed.
    '''

    # analyse_cols
    spalten = ['col_name', 'datatype_short', 'datatype_identified','mem_usage','nunique', 'ndups', 'vmin', 'vmax','n']
    
    analyse = pak.analyse_cols(  pak.sample(data_df, 10000), human_readable=False  )[spalten].iloc[1:]
    mask = analyse.col_name == 'split'
    analyse = pak.drop_rows(analyse,mask)
    analyse['is_output_feature'] = False
    analyse['feature_type'] = ''
    analyse = pak.move_cols(analyse,['is_output_feature','feature_type'],'col_name')
    analyse = pak.reset_index(analyse)

    # is_output_feature
    if dataset_loader is not None:
        output_feature_names = [col['name'] for col in dataset_loader.config.output_features]    
    else:
        output_feature_names = list(data_df.columns)[:output_features_size]
    mask = analyse.col_name.isin(output_feature_names)
    analyse.loc[mask,'is_output_feature'] = True

    # binary feature_type
    mask = analyse['nunique'] == 2
    analyse.loc[mask,'feature_type'] = 'binary'

    # category from number feature_type
    mask0 = analyse['datatype_identified'].isin(['int','float'])    
    mask1 = analyse['nunique'] / analyse['ndups'] < 0.05
    mask2 = analyse['nunique'] <= 30    
    mask3 = analyse.feature_type == ''
    mask = mask0  &  mask1  &  mask2  &  mask3
    analyse.loc[mask,'feature_type'] = 'category'

    # category from text feature_type
    mask0 = analyse['datatype_identified'].isin(['string']) 
    mask1 = analyse['nunique'] / analyse['ndups'] < 0.1
    mask2 = analyse['nunique'] <= 50    
    mask3 = analyse.feature_type == ''
    mask = mask0  &  mask1  &  mask2  &  mask3
    analyse.loc[mask,'feature_type'] = 'category'    

    # numeric feature_type
    mask1 = analyse['datatype_identified'].isin(['int','float'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'number'
    
    # vector feature_type
    try:
        pattern = r'^\s*(\d+(\.\d+)?\s*)+$'
        mask1 = analyse['datatype_identified'].isin(['string'])
        mask2 = analyse['vmin'].str.match(pattern)
        mask3 = analyse['vmax'].str.match(pattern)
        mask4 = analyse.feature_type == ''
        mask = mask1  &  mask2  &  mask3  &  mask4
        analyse.loc[mask,'feature_type'] = 'vector'
    except:
        pass
    
    # text feature_type
    mask1 = analyse['datatype_identified'].isin(['string'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'text'

    # image feature_type  
    try:
        mask1 = analyse['feature_type'] == 'text'
        mask2 = analyse['vmin'].str.endswith(('jpg','png'))
        mask3 = analyse['vmin'].str.endswith(('jpg','png'))        
        mask = mask1  &  mask2  &  mask3
        analyse.loc[mask,'feature_type'] = 'image'
    except:
        pass

    # date feature_type  
    mask1 = analyse['datatype_identified'].isin(['datetime'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'date'

    # sequence feature_type  
    mask1 = analyse['datatype_identified'].isin(['list'])
    mask2 = analyse.feature_type == ''
    mask = mask1 & mask2
    analyse.loc[mask,'feature_type'] = 'sequence'    

    # feature_type_guess
    #analyse['feature_type_guess'] = analyse.feature_type.copy()
    #analyse = pak.move_cols(analyse, 'feature_type_guess', 'feature_type')
    
    # überschreibe feature_type_real
    if dataset_loader is not None:
        output_features_real = pak.dataframe(dataset_loader.config.output_features)
        analyse = pak.update_col(analyse, output_features_real, left_on='col_name', right_on='name', col='type', col_rename='feature_type')    
    
    return analyse 





def config0(data_df, dataset_loader=None, output_features_size=1, use_yaml=True):
    '''
    Creates a default config for a given DataFrame. To identify the output_features, use
    * dataset_loader or 
    * output_features_size as in analyse_cols().
    '''
    analyse = analyse_cols(data_df, dataset_loader, output_features_size)
    mask = analyse.is_output_feature
    output_features_size = analyse[mask].shape[0]
    
    # input_features
    spalten = ['col_name','feature_type']
    input_features = analyse[output_features_size:][spalten]
    input_features.columns = ['name','type']
    input_features = input_features.to_dict(orient='records')  

    # output_features
    output_features = analyse[:output_features_size][spalten]
    output_features.columns = ['name','type']
    output_features = output_features.to_dict(orient='records')

    # config
    config = {'input_features':  input_features,
              'output_features': output_features }

    if use_yaml:
        return yaml.dump(config)
    return config



def config1(dataset_loader, use_yaml=True):
    '''
    Wrapper for default_model_config from dataset_loader
    '''
    result = dataset_loader.default_model_config

    if use_yaml:
        result = yaml.dump(result)
        result = result.replace( 'null\n...\n', '' )
        
    return result    


def configs(data_df, dataset_loader=None, output_features_size=1, use_yaml=True):
    '''
    List of config0, config1
    '''
    c0 = config0(data_df, dataset_loader=dataset_loader, output_features_size=output_features_size, use_yaml=use_yaml)
    if dataset_loader is not None:
        c1 = config1(dataset_loader,use_yaml=use_yaml)
    if dataset_loader is None or c1 is None or c1 == '':
        return [c0]
    else:
        return [c0,c1]



#def list_datasets():
#    '''
#    List all datasets available in Ludwig.
#    '''
#    def get_filelist(use_github=False):
#        if use_github:
#            repository_url = 'https://api.github.com/repos/ludwig-ai/ludwig/contents/ludwig/datasets/configs'
#            response = requests.get(repository_url)
#            directory_contents = response.json()
#            file_list = [item['name'] for item in directory_contents]  
#            return file_list
#        else:
#            library_location = pkg_resources.get_distribution('ludwig').location
#            directory_within_library = 'ludwig/datasets/configs'
#            directory_path = os.path.join(library_location, directory_within_library)
#            file_list = os.listdir(directory_path)       
#            return file_list            
#    try:
#        file_list = get_filelist(use_github=False)
#    except:
#        file_list = get_filelist(use_github=True)  
#        print('using github')
#    elements_to_remove = ['__pycache__','__init__.py']
#    result = [x.replace('.yaml','') for x in file_list if x not in elements_to_remove]
#    result = sorted(result)
#
#    return result







def scan_datasets( dataset_names, use_cache=False ):
    '''
    Scan and analyse Ludwig's database zoo. 
    '''
    pickle_filename = 'scan_datasets.temp.pickle'
    if use_cache:
        try:
            return pak.load_pickle(pickle_filename)   
        except:
            print('cache error')
            return scan_datasets( dataset_names, use_cache=False )
        
    result = []
    
    for dataset in dataset_names:
        
        # load_dataset
        print('loading',dataset)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")            
                data_df, dataset_loader = load_dataset(dataset, verbose=False)  

            # analysieren 
            analyse = analyse_cols(data_df, dataset_loader) 
            mask = analyse.is_output_feature
            output_features_size = analyse[mask].shape[0]        
    
            # output_features and input_features 
            spalten = ['col_name','feature_type','mem_usage']
            output_features = analyse[:output_features_size][spalten]           
            input_features = analyse[output_features_size:][spalten]        
    
            # Ausgabewerte berechnen
            input_features_type  = ', '.join(pak.group_and_agg( input_features,  ['feature_type','mem_usage'], ['','sum']).sort_values('mem_usage_sum', ascending=False).feature_type)
            output_features_type = ', '.join(pak.group_and_agg( output_features, ['feature_type','mem_usage'], ['','sum']).sort_values('mem_usage_sum', ascending=False).feature_type)        
    
            # Ausgabe
            result += [{'dataset_name': dataset, 
                        'status'      : 'ok',
                        'rows'        : bpy.human_readable_number(data_df.shape[0]) ,
                        'in_size'     : input_features.shape[0],                        
                        'out_size'    : output_features.shape[0],
       
                        'in_name'     : ', '.join(input_features.col_name),                    
                        'out_name'    : ', '.join(output_features.col_name),                    
       
                        'in_type'     : input_features_type,  # ', '.join(input_features.feature_type),                      
                        'out_type'    : output_features_type, # ', '.join(output_features.feature_type),                    
                                     
                        'description' : dataset_loader.description(),
                        'config1'     : config1(dataset_loader),
    
                       }]

        except:
            result += [{'dataset_name': dataset, 
                        'status'      : 'Error load',
                        'rows'        : 0 ,
                        'in_size'     : 0,                        
                        'out_size'    : 0,
       
                        'in_name'     : '',                    
                        'out_name'    : '',                    
       
                        'in_type'     : '',                       
                        'out_type'    : '',                    
                                     
                        'description' : '',  
                        'config1'     : '',  
    
                       }]
    
    result = pak.dataframe(result) 

    if not use_cache:
        pak.dump_pickle(result,pickle_filename)
    return result



        
#####################################################################################################
# train_log
#


def train_log(train_log_raw, T=False):
    ''' returns small log'''
    if train_log_raw.shape[0] > 0:
        result = prepare_train_log(train_log_raw, size='small')
    else:
        zeilen = ['validation_metric','loss','roc_auc','accuracy','recall','specificity','precision','epochs','time/epoch','train_time']
        result = pd.DataFrame(zeilen)
        result.columns = ['name']
    if not T:
        return result
        
    result = result.set_index('name')
    result = result.T.reset_index()
    result = pak.rename_col(result,'index','model')
    return result



def train_log_big(train_log_raw):
    ''' returns bigger log'''
    return prepare_train_log(train_log_raw, size='big')        


    
def train_log_to_csv(train_log_raw):
    '''
    Saves train_log_big to csv file
    Saves train_log_raw to csv file
    Shows train_log (small version)
    '''
    t0 = train_log_raw
    t1 = train_log_big(train_log_raw)
    t2 = train_log(train_log_raw)
    
    t0.to_csv( 'train_log_raw.csv', index=False) 
    t1.to_csv( 'train_log_big.csv', index=False)  
    t2.to_csv( 'train_log.csv',     index=False)       
    return t2



def prepare_train_log(train_log_raw, size='small'):

    # target_value ergänzen
    mask = train_log_raw.name == 'validation_metric'  
    validation_metrics = train_log_raw[mask]
    
    mask = pak.isin(train_log_raw, validation_metrics, left_on=['model_name','name'], right_on=['model_name','value'])
    df = train_log_raw[mask].copy()
    df['name'] = 'target_value'
    train_log_raw = pak.add_rows(train_log_raw, df, only_new=['model_name','name','value'])
    
    result = pd.pivot_table( train_log_raw, 
                              index='name',
                              columns='model_name',
                              values='value', 
                              aggfunc='last')
    result = pak.drop_multiindex(result).reset_index() 
    
    # Namen korrigieren
    mask = result.name.str.startswith('average')
    result.loc[mask,'name'] = result[mask].name.str.replace('average_','') + '_avg'   


    # Zeilen sortieren
    if size == 'small':
        zeilen_vorne =  ['target_value','validation_metric','loss','accuracy','recall','specificity','precision','roc_auc',]
        zeilen_hinten = ['epochs','time/epoch','train_time',]    
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )      
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()

        # Zeilen löschen
        zeilen_verboten = []
        zeilen_erlaubt = [z for z in ( zeilen_vorne + zeilen_hinten) if not z in zeilen_verboten ]
        mask = result.name.isin( zeilen_erlaubt )
        result = result[mask]
        
    else: # size == 'big'
        result = result.sort_values('name')
        zeilen_vorne =  ['target_value','validation_metric','loss',]
        zeilen_hinten = ['experiment_name','experiment_path','output_feature_type','output_feature_name','epochs','train_secs','time/epoch','train_time',]     
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )         
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()        

    result = pak.reset_index(result)
    result.columns = [c if isinstance(c,str) else 'model_' + str(c) for c in result.columns ]
    return result







