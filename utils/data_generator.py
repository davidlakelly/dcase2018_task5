from email.mime import audio
import numpy as np
import h5py
import time
import csv
import logging

from utilities import calculate_scalar, scale
import config


class DataGenerator(object):
    
    def __init__(self, hdf5_path, batch_size, train_txt=None, 
                 validate_txt=None, seed=1234):
        """Data generator. 
        
        Args:
          hdf5_path: string, path of development hdf5
          batch_size: int
          train_txt: string | None, if None then all audios are used for 
            training
          validate_txt: string | None, if None then all audios are used for 
            training
          seed: int, random seed
        """
        # print(train_txt)
        # if(validate_txt==None):
        #     print("No text found")
        # else:
        #     print("found text")
        #     print(validate_txt)
        self.random_state = np.random.RandomState(seed)
        self.validate_random_state = np.random.RandomState(0)
        lb_to_ix = config.lb_to_ix

        self.batch_size = batch_size
        
        # Load data
        load_time = time.time()
        hf = h5py.File(hdf5_path, 'r')
        #hf_a = h5py.File("C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\aug_shuffle_ten_per\\features\\logmel\\development.h5", 'r')
        
        
        self.audio_names = np.array([
            name.decode() for name in hf['audio_name']])
        
        # self.audio_names2 = np.array([
        #     name.decode() for name in hf_a['audio_name']])
        
        # self.audio_names = np.concatenate((self.audio_names,self.audio_names2),axis=0) 
        
       
        self.x = hf['feature'][:]
        # self.x_a = hf_a['feature'][:]
        # self.x = np.concatenate((self.x, self.x_a), axis=0)
        
        
        print(type(hf))
        target_labels = [label.decode() for label in hf['label']]
        # target_labels_a = [label.decode() for label in hf_a['label']]
        # target_labels = np.concatenate((target_labels,target_labels_a), axis=0)

        
        self.y = np.array([lb_to_ix[label] for label in target_labels])
        
        logging.info("Load data time: {}".format(time.time() - load_time))
        
        # Get audio ids for training and validation
        if train_txt is None or validate_txt is None:
            self.train_audio_indexes = np.arange(len(self.audio_names))
            self.validate_audio_indexes = np.array([])
            print("This should not run")
            
        else:
            get_index_time = time.time()
            self.train_audio_indexes = self.get_audio_indexes(train_txt)
            self.validate_audio_indexes = self.get_audio_indexes(validate_txt)
            # print(self.train_audio_indexes.size)
            # print(self.validate_audio_indexes.size)
            logging.info('Get indexes time: {:.3f} s'.format(
                time.time() - get_index_time))
        logging.info('Training audios: {}'.format(
            len(self.train_audio_indexes)))
            
        logging.info('Validation audios: {}'.format(
            len(self.validate_audio_indexes)))
        
        # Scalar
        (self.mean, self.std) = calculate_scalar(
            self.x[self.train_audio_indexes])
        
        hf.close()
        
    def get_audio_indexes(self, txt_file, train=False):
        
        audio_names = self.audio_names
        audio_names_in_txt = []
        
        # Read filenames in txt file
        with open(txt_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            lis = list(reader)
            if train:
                path = "C:\\Users\\David\\Desktop\\dcase_5\\dcase2018_task5\\DCASE2018-task5-dev\\aug\\aug_shuffle_ten_per\\aug_shuffle_ten_per_meta.txt"
                with open(path,"r") as aug:
                    t_read = csv.reader(aug, delimiter='\t')
                    lis.extend(list(t_read))
            
            audio_names_in_txt = [li[0].split('/')[1] for li in lis]
        # print(audio_names_in_txt)
                
        # Get audio ids correspondent with the txt file
        ids = []
                
        for (i1, audio_name) in enumerate(audio_names):
            if audio_name in audio_names_in_txt:
                # print("found match")
                ids.append(i1)
            else:
                pass
                # print("no match")
                # print(audio_name)
        
        ids = np.array(ids)
        
        return ids

    def transform(self, x):
        
        return scale(x, self.mean, self.std)
        
    def generate_train(self):
        
        batch_size = self.batch_size
        indexes = np.array(self.train_audio_indexes)
        
        self.random_state.shuffle(indexes)
        
        iteration = 0
        pointer = 0
        
        while True:
            
            # Reset pointer
            if pointer >= len(indexes):
                pointer = 0
                self.random_state.shuffle(indexes)
            
            # Get batch indexes
            batch_audio_indexes = indexes[pointer : pointer + batch_size]
            pointer += batch_size
            
            iteration += 1
            
            batch_x = self.x[batch_audio_indexes]
            batch_y = self.y[batch_audio_indexes]
            
            batch_x = self.transform(batch_x)
            
            yield batch_x, batch_y
        
    def generate_validate(self, data_type, shuffle, max_iteration=None):
        """Generate mini-batch data for validation. 
        
        Args: 
          data_type: 'train' | 'validate'
          shuffle: bool
          max_iteration: None | int, maximum iteration to speed up validation
        """
    
        batch_size = self.batch_size
        
        if data_type == 'train':
            indexes = np.array(self.train_audio_indexes)
            
        elif data_type == 'validate':
            indexes = np.array(self.validate_audio_indexes)
            
        else:
            raise Exception("Invalid data_type!")
        
        if shuffle:
            self.validate_random_state.shuffle(indexes)
        
        iteration = 0
        pointer = 0
        
        while True:
            
            if iteration == max_iteration:
                break
            
            # Reset pointer
            if pointer >= len(indexes):
                break
            
            # Get batch ids
            batch_audio_indexes = indexes[pointer : pointer + batch_size]
            pointer += batch_size
            
            iteration += 1
            
            batch_x = self.x[batch_audio_indexes]
            batch_y = self.y[batch_audio_indexes]
            batch_audio_names = self.audio_names[batch_audio_indexes]
            
            batch_x = self.transform(batch_x)
            
            yield batch_x, batch_y, batch_audio_names
            
            
class TestDataGenerator(DataGenerator):
    
    def __init__(self, dev_hdf5_path, test_hdf5_path, batch_size):
        """Testing data generator. 
        
        Args:
          dev_hdf5_path: string, path of development hdf5
          test_hdf5_path: string, path of test hdf5
          batch_size: int
        """
        
        super(TestDataGenerator, self).__init__(hdf5_path=dev_hdf5_path, 
                                                batch_size=batch_size)
                                                
        # Load data
        load_time = time.time()
        hf = h5py.File(test_hdf5_path, 'r')
        
        self.test_audio_names = np.array(
            [name.decode() for name in hf['audio_name']])
        
        self.test_x = hf['feature'][:]
        
        logging.info("Load data time: {}".format(time.time() - load_time))
        
    def generate_test(self):
        
        audios_num = len(self.test_audio_names)
        audio_indexes = np.arange(audios_num)
        batch_size = self.batch_size
        
        pointer = 0
        
        while True:

            # Reset pointer
            if pointer >= audios_num:
                break

            # Get batch indexes
            batch_audio_indexes = audio_indexes[pointer: pointer + batch_size]
                
            pointer += batch_size

            batch_x = self.test_x[batch_audio_indexes]
            batch_audio_names = self.test_audio_names[batch_audio_indexes]

            # Transform data
            batch_x = self.transform(batch_x)

            yield batch_x, batch_audio_names