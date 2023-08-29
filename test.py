def multiprocess_cml(self, chunk, process, new_base, df_output):
        # use cml to get the result then replace the original result
        for i in [x.split('-') for x in chunk['CASE'].values]:
            ab = new_base.loc[new_base['CASE'] == '-'.join(i)] 
            GenerateCase().reverse_to_raw_cases(ab.iloc[:,1:], self.base_case, ab.iloc[:,1:-len(df_output.columns[1:])].columns.tolist(), f'C:/Users/M/Desktop/2/data/{process}/data', '-'.join(i))
        
        y = main_cml(f'C:/Users/M/Desktop/2/data/{process}')
        
        dat_files = glob.glob(f'C:/Users/M/Desktop/2/data/{process}/data/*.dat')
        for r in dat_files:
            os.remove(r)
        
        return y

    def multi_p(self,new_base, df_output):
        pool = multiprocessing.Pool()
    
        chunks = []
        df_size = len(new_base) // 12
    
        for i in range(13):
            start_idx = i * df_size
            end_idx = start_idx + df_size if i < 12 else None
            chunks.append(new_base[start_idx:end_idx])
    
        results = []
        for i, chunk in enumerate(chunks):
            process_name = f'p{i+1}'
            result = pool.apply_async(self.multiprocess_cml, args=(chunk, process_name, new_base, df_output))
            results.append(result)
    
        pool.close()
        pool.join()
    
        yconcat = pd.concat([result.get() for result in results], axis=0, ignore_index=True)
        
        return yconcat
