import pandas as pd
class MatlabData:

    def __init__(self, data):
        # Extract data fields
        self.id = data["o"]["id"][0][0][0]
        self.tag = data["o"]["tag"][0][0]
        self.nS = data["o"]["nS"][0][0][0]
        self.sampFreq = data["o"]["sampFreq"][0][0][0][0]
        self.marker = pd.DataFrame(data["o"]["marker"][0][0])
        self.timestamp = data["o"]["timestamp"][0][0]
        self.data =(pd.DataFrame(data["o"]["data"][0,0]))
        self.trials = data["o"]["trials"][0][0]
        self.mapped_data = self.mapping_data(self.data)



    def __repr__(self):
        return (f"MatlabData(\n"
                f"  ID: {self.id},\n"
                f"  Tag:  {self.tag},\n"
                f"  Number of Samples: {pd.DataFrame(self.nS)},\n"
                f"  Sampling Frequency: {self.sampFreq},\n"
                f"  Marker shape: {self.marker},\n"
                f"  Timestamp shape: {self.timestamp.shape},\n"
                f"  Data_mapped : {pd.DataFrame(self.mapped_data)},\n"
                f"  Trials shape (batch size, channels ,Số lượng trials,time steps hoặc samples)  : {self.trials.shape}\n"
                f")")
    @staticmethod
    def mapping_data(dataframe):
      new_names = ['ED_COUNTER' ,'ED_INTERPOLATED', 'ED_RAW_CQ', 'AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8','T8', 'FC6','F4','F8','AF4','GYROX','GYROY','ED_TIMESTAMP','ED_ES_TIMESTAMP','ED_FUNC_ID','ED_FUNC_VALUE','ED_MARKER','ED_SYNC_SIGNAL']
      if len(dataframe.columns) != len(new_names):
          raise ValueError("Số lượng cột trong DataFrame và số lượng tên mới không khớp.")
      dataframe.columns = new_names
      return dataframe
