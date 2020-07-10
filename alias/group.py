
import concurrent.futures
import time


# TINY GROUPER TO RUN CONCURRENT
class Group:
    def __init__( self , *args , **kwargs ):
        self.group = args[0]

    def __getattr__( self, name ):
        def _missing(*args, **kwargs):
            #ar = self.run_concurrent( self.group , name )
            ar = self.run_serial( self.group , name )
            return ar
        return _missing

    def gather(self, method_name ):
        print(' ')

    def run_concurrent_generator(self , obj_arr_in , method_name ):
        print( 'this will return generator to iterate async ')


    def run_serial(self , obj_arr_in , method_name ):
        outputs = []
        for x in obj_arr_in:
            method_output = getattr( x , method_name )()
            if( method_output != False ):
                outputs.append( method_output )
        return outputs

    def run_concurrent( self, obj_arr_in , method_name ):
        result_array=[]
        start_time = time.time()
        linenum=0
        with concurrent.futures.ThreadPoolExecutor( max_workers=100 ) as executor:
            futures_generator = ( executor.submit( getattr( obj,method_name ) ) for obj in obj_arr_in )
            completed_que  = concurrent.futures.as_completed( futures_generator )
            for future in completed_que:
                try:
                    data = future.result()
                    #print( str(linenum)+' : '+ data['domain']+' '+ str( time.time() - start_time  ) )
                    print( str(linenum)+' : '+ str( time.time() - start_time  ) )
                    linenum=linenum+1
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    if( data != False ):
                        result_array.append(data)
        return result_array
