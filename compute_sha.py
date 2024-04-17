import hashlib
import pandas


def KEY2ID(k):
    return hashlib.sha256(k.encode("utf-8")).hexdigest()


def main():
    
    df = pandas.DataFrame(
        {
            'Region': ['1A'],
            'Product': ['DISTILLATES'],
            'Grade': ['#1 Diesel'],
            'SubGrade': ['BioVolume'],
        }
    )
    
    column_name = 'instrument_id'
    columns = [ column for column in df.columns ]
    hash_fn = KEY2ID
    
    def concat_str(r):
        return "".join(map(str, r))

    # def map_partition_func(df):
    #     outputs = map(hash_fn, map(concat_str, df[columns].to_numpy()))
    #     return pandas.DataFrame(data=outputs, index=df.index, columns=[column_name])

    # def map_partition_func(df):
    #     #outputs = map(hash_fn, map(concat_str, df[columns].to_numpy()))
    #     l = ['1A', 'DISTILLATES', '#1 Diesel', 'BioVolume']
    #     #s = pandas.Series(l)
    #     #outputs = map(hash_fn, map(concat_str, s.to_numpy()))
    #     outputs = map(hash_fn, map(concat_str, l))
    #     return pandas.DataFrame(data=outputs, index=df.index, columns=[column_name])
    
    def map_partition_func():
        column_names = ['Region', 'Product', 'Grade', 'SubGrade']
        column_name_to_index = {}
        for i in range(len(column_names)):
            column_name = column_names[i]
            column_name_to_index[column_name] = i
        values = ['1A', 'DISTILLATES', '#1 Diesel', 'BioVolume']
        column_names = sorted(column_names)
        ordered_values = []
        for column_name in column_names:
            index = column_name_to_index[column_name]
            value = values[index]
            ordered_values.append(value)
        string = concat_str(ordered_values)
        # Region Product Grade SubGrade
        # Ordered: Grade, Product, Region, SubGrade,
        #string = '#1 DieselDISTILLATES1ABioVolume'
        return hash_fn(string)
    
    # df_with_hash = map_partition_func(df)
    # df = df_with_hash
    # hash_str = df[column_name][0]
    hash_str = map_partition_func()
    print(f'hash_str={hash_str}')
    

if __name__ == '__main__':
    main()