## 背景
想在Windows系统里使用python的multiprocessing真可谓一波三折，小坑多多，不过最终还是能实现。尽量能在Linux环境下使用，毕竟不用费心。

## 任务
本次任务为了在Windows环境下使用python的multiprocessing，以提升效率。任务要求是通过多进程（这里使用了13个进程）来获取某函数的数据处理结果，也就是函数会return一组数据，最后将所有return的数据combine.

## 代码部分
### 代码1
1.这里使用了13个进程来运行函数multiprocess_cml，该函数会处理数据并最终返回一个dataframe
2.new_base[start_idx:end_idx]类似于一个分页，例如100条数据，第一个进程拿0~10条，第二个进程拿11~20去run...如此类推。
3.以下代码可以稍作修改直接食用。

```python
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
```
### 代码2
在Windows下使用multiprocessing必须在<font size=5 color=RED>if __name__ == '__main__':</font> 



