
import logging, os, shutil, time, yaml, warnings, json
import pandas as pd
import bpyth as bpy

from munch import DefaultMunch

from ludwig.api       import LudwigModel
from ludwig.visualize import learning_curves
from ludwig.visualize import compare_performance
from ludwig.visualize import confusion_matrix
from ludwig.visualize import roc_curves_from_test_statistics
from torchinfo        import summary

from bludwig.helper import *

# logging.DEBUG   == 10
# logging.INFO    == 20
# logging.WARNING == 30


# LudwigJob wird einmal instanziiert
#
class LudwigJob():

    
#####################################################################################################
# Basics
#     
    
    def __init__( self, configs=[], experiment_name=None, verbose=False ):  
        '''
        LudwigJob wird einmal instanziiert, z.B. so:
        ludwig_job = bludwig.LudwigJob( configs=configs, verbose=True) 
        * configs: list of Ludwig-configs as YAML-String, Path to yaml-file or yaml-object
            
        '''
        # Parameter         
        if experiment_name is None:
            experiment_name = 'model'
        self.experiment_name = experiment_name
        self.verbose = verbose        

        # configs ggf. in YAML wandeln
        self.configs = []
        for config in configs:
            if isinstance(config, str):
                if config.count('\n') > 2: 
                    self.configs += [yaml.safe_load(config)]
                else:
                    self.configs += [config]   

        try:
            import google.colab
            self.in_colab = True 
        except:
            self.in_colab = False     

        # Tensorflow warnings unterdrücken
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    

        # gpu_info
        if verbose:
            gpu_info()

        # aktuelles model
        self.model = None
        self.model_no = None
        self.cuda = None
        self.output_feature_name = ''

        # job
        self.train_jobs = []
        self.model_names = []
        self.model_paths = []

        # train_log
        self.train_log = pd.DataFrame()


        # results
        self.train_stats      = []
        self.test_stats       = []
        self.output_dirs      = []       

        if len(configs) > 0:
            print()
            print('{} configs loaded'.format(len(configs)))



    def __str__(self):
        result = f'''LudwigJob object
        experiment_name:     {self.experiment_name}
        output_feature_name: {self.output_feature_name}
        train_jobs:          {self.train_jobs}
        model_names:         {self.model_names}
        model_paths:         {self.model_paths}        
        output_dirs:         {self.output_dirs}
        model_no:            {self.model_no}   
        cuda:                {self.cuda}             
        '''
        return result


    
    def load_from_results(self, experiment_name=None):    
        '''
        Loads data from results directory
        * experiment_name: Only load results from this experiment. Otherwise all.
        '''
        results_dir = sorted(os.listdir('results'))
        if experiment_name is not None:
            results_dir = [rd for rd in results_dir if rd.startswith(experiment_name)]
        self.output_dirs = [ 'results/' + d                for d in results_dir ]
        self.train_jobs  = [ int(d.split('_')[-2])         for d in results_dir ]
        self.model_names = [ self.experiment_name + '_' + str(j)             for j in self.train_jobs ]    
        self.model_paths = [d + '/model'                   for d in self.output_dirs]
        
        train_stats = [ d + '/training_statistics.json'    for d in self.output_dirs ]
        train_stats = [ json.load( open(p) )               for p in train_stats]
        self.train_stats = [ DefaultMunch.fromDict(d)      for d in train_stats]

        test_stats = [ d + '/test_statistics.json'         for d in self.output_dirs ]
        test_stats = [ json.load( open(p) )                for p in test_stats]
        self.test_stats = [ DefaultMunch.fromDict(d)       for d in test_stats]

        # output_feature_name
        a = list(self.test_stats[0].keys())
        a.remove('combined')
        self.output_feature_name = a[0]   
        # nochmal gegenprüfen
        b = list(self.train_stats[0]['test'].keys())
        b.remove('combined')
        assert self.output_feature_name in b


    
    def load_model(self, model_no, cuda=True):
        '''
        Loads a model identified by model number.
        * cuda: Use cuda, if available
        '''
        if model_no == self.model_no and cuda == self.cuda:
            return
            
        self.model = LudwigModel.load( self.model_paths[model_no] )
        if cuda and torch.cuda.is_available():
            self.model.model.to('cuda')
            self.cuda = True
        else:
            self.model.model.to('cpu')   
            self.cuda = False
        self.model_no = model_no




        
#####################################################################################################
# print_models
#

    def print_model(self, model_no=None):
        '''
        Uses torchinfo.summary to print a model
        '''
        if model_no is None:
            model_no = self.model_no
        self.load_model(model_no, cuda=False)
        print( '### {} ###'.format(self.model_names[model_no]))
        print( summary(self.model.model, 
                       input_data=[self.model.model.get_model_inputs()], 
                       depth=20, 
                       col_names=['input_size','output_size','num_params','trainable'] 
                      ) )
        print('\n'*3)   


    
    def print_models(self):        
        for model_no in self.train_jobs:
            self.print_model(model_no)

            
        
#####################################################################################################
# experiment
#
    
    def experiment(self, dataset, train_jobs=None, count_runs=[0] ):
        '''
        train and evaluate a list of Ludwig models
        '''
        
        # counts calls of this function
        count_runs[0]+=1  
        
        if train_jobs is None:
            train_jobs = [ no for (no, _) in enumerate(self.configs)]        
        self.train_jobs = train_jobs
        self.model_names = [self.experiment_name + '_' + str(config_no) for config_no in train_jobs]
        
        
        for config_no in train_jobs:
            self.model_name          = self.model_names[config_no]
            self.model_no            = config_no
            
            experiment_path = 'results/' + self.model_name + '_run'  
            print()
            print( 'Training model {}'.format(self.model_name) )   
            
            # Zielverzeichnis rekursiv löschen
            try:
                shutil.rmtree(experiment_path)
            except:
                pass

            logging_level = 20 if self.verbose else 30

            # lade model
            self.model               = LudwigModel(config=self.configs[config_no], logging_level=logging_level)   

            
            self.cuda                = torch.cuda.is_available()
            self.output_feature_name = self.model.config['output_features'][0]['name']
            self.output_feature_type = self.model.config['output_features'][0]['type']

            # trainiere
            start_time = time.time()     
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")            
                test_stat, train_stat, _, output_dir = self.model.experiment( dataset=dataset, experiment_name=self.model_name)
            self.test_stats  += [test_stat]
            self.train_stats += [train_stat]
            self.output_dirs += [output_dir]
            self.model_paths += [output_dir + '/model']

            # logge config
            train_secs        = round( time.time() - start_time )
            train_time        = bpy.human_readable_seconds( train_secs )
            epochs            = len(train_stat.test['combined']['loss']) 
            validation_metric = self.model.config['trainer']['validation_metric']
            log = pak.dataframe([
                [ count_runs[0], self.model_name, 'experiment_name',     self.experiment_name   ],                
                [ count_runs[0], self.model_name, 'train_secs',          train_secs        ],
                [ count_runs[0], self.model_name, 'train_time',          train_time        ],
                [ count_runs[0], self.model_name, 'epochs',              epochs            ],
                [ count_runs[0], self.model_name, 'time/epoch',          bpy.human_readable_seconds( train_secs/epochs ) ],     
                [ count_runs[0], self.model_name, 'validation_metric',   validation_metric ],     
                [ count_runs[0], self.model_name, 'experiment_path',     experiment_path   ], 
                [ count_runs[0], self.model_name, 'output_feature_name', self.output_feature_name   ],    
                [ count_runs[0], self.model_name, 'output_feature_type', self.output_feature_type   ],                    
                
            ])
            log.columns = ['run','model_name','name','value']
            log2 = analyse_test_stat( count_runs[0], self.model_name, test_stat)
            self.train_log = pak.add_rows( self.train_log, log  )             
            self.train_log = pak.add_rows( self.train_log, log2 ) 
            
            print('train_time:',train_time) 
            print()
       



        
#####################################################################################################
# predict
#

    def predict(self, data, merge=True):
        pred, _ = self.model.predict(data)
        if not merge:
            return pred
            
        pred.index = data.index
        result = pd.merge( data, pred, left_index=True, right_index=True)
        result = pak.move_cols( result, [self.output_feature_name, self.output_feature_name + '_predictions'])
        result.rename(columns=lambda x: x.replace('_predictions', '_pred').replace('probabilities', 'prob').replace('probability', 'prob'), inplace=True)
        return result        





        
        
#####################################################################################################
# Visualisierungen
#

    def compare_performance(self, output_feature_name=None):

        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name
        
        # test_stats_small (verhindert Fehler)
        test_stats_small = []
        try:
            keys_to_keep = set(self.train_log.name)
        except:
            keys_to_keep = {'accuracy','accuracy_micro','roc_auc','loss'}
        for stat in self.test_stats:
            r = {key: value  for key, value in stat[output_feature_name].items()  if key in keys_to_keep}
            r = { output_feature_name: r }    
            test_stats_small += [r]    

        # ausgeben
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            compare_performance( test_stats_small, model_names=self.model_names, output_feature_name=output_feature_name )


    
    def learning_curves(self, output_feature_name=None):
        
        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name    
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            learning_curves( self.train_stats, model_names=self.model_names, output_feature_name=output_feature_name)     


    
    def confusion_matrix(self, output_feature_name=None, normalize=True, top_n_classes=[10]):

        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name  

        #load_model
        if self.model is None:
            try:
                self.load_model(0)
            except:
                print('No model loaded')
            
        # confusion_matrix
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            confusion_matrix( self.test_stats, 
                              self.model.training_set_metadata, 
                              output_feature_name=output_feature_name, 
                              top_n_classes=top_n_classes, 
                              model_names=self.model_names, 
                              normalize=True )


    
    def roc_curves(self, output_feature_name=None):
        '''
    
        '''
        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name  
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                roc_curves_from_test_statistics(self.test_stats, output_feature_name=output_feature_name)   
            except KeyError:
                print('No roc_curve found')
                pass
            except TypeError:
                print('No roc_curve found')
                pass                
            except:
                raise  # Löst die Ausnahme erneut aus        
                



