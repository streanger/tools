import sys
import os


class StrangeTools():
    '''need to be developed, to help with many stuff'''
    def __init__(self):
        self.script_path = os.path.realpath(os.path.dirname(__file__))
        self.current_path = ''
        self.dir_sequence = []
        
        
    def switch_dir(self, directory):
        '''it switch to specified directory. If directory is not specified it creates it'''
        
        if not self.current_path:
            self.current_path = self.script_path
            os.chdir(self.current_path)
            self.dir_sequence = [self.current_path]
            
        if directory == '.':
            self.current_path = self.script_path
            os.chdir(self.current_path)
            self.dir_sequence = [self.current_path]
            return self.current_path
            
        if directory == '..':
            if len(self.dir_sequence) < 2:
                return self.current_path
                
            self.dir_sequence = self.dir_sequence[:-1]
            self.current_path = os.path.join(*self.dir_sequence)
            os.chdir(self.current_path)
            return self.current_path
            
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        self.current_path = os.path.join(self.current_path, directory)
        os.chdir(self.current_path)
        
        self.dir_sequence.append(directory)
        return self.current_path
        
        
if __name__ == "__main__":
    strange = StrangeTools()
    strange.switch_dir('MAIN')
    strange.switch_dir('LEFT')
    strange.switch_dir('VERY_LEFT')
    strange.switch_dir('..')
    strange.switch_dir('..')
    strange.switch_dir('RIGHT')
    strange.switch_dir('VERY_RIGHT')
    strange.switch_dir('.')
    strange.switch_dir('TEST')
    
    