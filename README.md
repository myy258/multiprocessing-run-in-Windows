## 背景
想在Windows系统里使用python的multiprocessing真可谓一波三折，小坑多多，不过最终还是能实现。尽量能在Linux环境下使用，毕竟不用费心。


## 任务
本次任务为了在Windows环境下使用python的multiprocessing，以提升效率。任务要求是通过多进程（这里使用了13个进程）来获取某函数的数据处理结果，也就是函数会return一组数据，最后将所有return的数据combine.


## 代码部分
#### 代码1

- 1.这里使用了13个进程来运行函数multiprocess_cml，该函数会处理数据并最终返回一个dataframe
- 2."new_base[start_idx:end_idx]"类似于一个分页，例如100条数据，第一个进程拿第0至10条，第二个进程拿第11至20去run...如此类推。
- 3.以下代码可以稍作修改直接食用。

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

#### 代码2
- 在Windows下使用multiprocessing必须在if __name__ == '__main__':之下，注意是必须！当然，如果你的multiprocessing只是用在子函数或者子子子函数中，则需要确保主函数在if __name__ == '__main__':之下就行。

```python
if __name__ == '__main__':
    multi_p() 
```

还有一点就是我们不再直接在任何IDE中直接运行代码（目前我认知中是不能的，如果能，恕我孤陋寡闻），会报错。必须在命令窗口使用命令运行（python main.py）
先键盘Win+R ----> cd至脚本文件目录下 ------> python main.py 完成
相当鸡肋啊~~debug难度大大增加

![image](https://github.com/myy258/multiprocessing-run-in-Windows/blob/main/Screenshot%202023-08-29%20163606.png) 


## 声明
如果代码能帮到你，请随便使用。本代码仅作为笔记或经验知识分享。




