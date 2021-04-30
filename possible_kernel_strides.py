def possible_pairs(steps, prediction_steps):
  result_list = []
  for strides in [2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
    for kernel in list(range(2,prediction_steps+1)):
      tmp_dev = steps/strides
      if steps%strides==0:
        tmp_dev -= 1
      elif steps%strides!=0:
        tmp_dev = np.floor(tmp_dev)

      result = tmp_dev*strides + (kernel-strides)
      if result==steps:
        result_list += [[kernel,strides]]
        print(result==steps, steps, result, 'strides: ', strides, 'kernel_size: ', kernel)
  return result_list

a = possible_pairs(100,10)
