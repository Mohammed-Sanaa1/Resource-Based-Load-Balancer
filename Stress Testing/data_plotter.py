import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib

matplotlib.use(backend='tkAgg')

def plot_data(df:pd.DataFrame, name="", save_as_image=False, display_graph=False):
#set the number of rows and columns for the subplot grid
    GRAPH_ROWS = 4
    GRAPH_COLUMNS = 1

    #create a figure and axes with 4 rows and 1 column
    fig, ax = plt.subplots(GRAPH_ROWS, GRAPH_COLUMNS, figsize=(7, 7))  # Adjust size as needed
    fig.suptitle(f"{name}'s statistics")

    #plot 1: error rate vs total requests sent
    ax1 = ax[0]
    ax1.set_xlabel('Time (in seconds)')
    ax1.set_ylabel('Error Rate (%)', color='tab:red')
    ax1.set_ylim(bottom=0)  #ensure the y-axis starts from 0
    ax1.plot(df['error_rate'], color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Total Requests Sent', color='tab:blue')
    ax2.plot(df['total_requests_sent'], color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    ax1.set_title('Error rate overtime')
#############################################################################
    #plot 2:  successful vs dropped requests
    ax2 = ax[1]
    ax2.set_xlabel('Time (in seconds)')
    ax2.plot(df.index, df['successful_requests'], color="green", label="successful requests")
    ax2.plot(df.index, df['failed_requests'], color="red", label="failed requests")
    ax2.set_title("Requests' status graph")
    ax2.legend(framealpha=0.5, bbox_to_anchor=(1, 1))
#############################################################################
    #plot 3: peak response and mean response times
    ax3 = ax[2]
    ax3.set_xlabel('Time (in seconds)')
    ax3.plot(df.index, df['peak_response_time'], color="red", label = "Peak response time (in seconds)")
    ax3.plot(df.index, df['mean_response_time'], color="purple", label="Mean response time (in seconds)")
    ax3.set_title('Reponse times graph')
    ax3.legend(framealpha=0.5, bbox_to_anchor=(1, 1))
    
#############################################################################
    #plot 4: pc specifications
    ax4 = ax[3]
    ax4.set_title("PC SPECS")
    ax4.axis('off')
    
    import cpuinfo, psutil, platform
    cpu = cpuinfo.get_cpu_info()
    memory_info = psutil.virtual_memory()
    ram = memory_info.total / (1024 ** 2)
    
    if 'brand_raw' in cpu and cpu['brand_raw']:
           #use brand_raw safely
           brand_raw_value = cpu['brand_raw']
    else:
        if 'hz_advertised_friendly' in cpu and cpu['hz_advertised_friendly']:
            brand_raw_value = f'{cpu["arch"]} {cpu["count"]}*CPU: {cpu["hz_advertised_friendly"]}'
        else:
            brand_raw_value = f'{cpu["arch"]} {cpu["count"]}*CPU: {cpu["hz_advertised"]}'
       
       
    info_text = f"{platform.system()} {platform.release()}: {platform.version()}\n{brand_raw_value}\n{int(ram)} MB RAM\n"
    ax4.text(0.5,0.5, info_text, horizontalalignment='center', verticalalignment='center')
        
    
    #adjust layout to prevent overlap
    plt.tight_layout()

    if (display_graph):
        #show the plot
        plt.show()
    
    if (save_as_image):
        import os
        dir_path = './output_fig'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        fig.savefig(f'{dir_path}/fig_{name}')
        print(f'Figure saved as {dir_path}/fig_{name}.png')