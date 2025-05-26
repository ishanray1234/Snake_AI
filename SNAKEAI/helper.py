import matplotlib.pyplot as plt
from IPython import display

plt.style.use('dark_background')
plt.ion()  # Enable interactive mode for live updates

def plot(scores, mean_scores):
    display.clear_output(wait=True)  # Clear the output for live updates
    display.display(plt.gcf())  # Display the current figure
    plt.clf()  # Clear the current figure

    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score', color='blue')
    plt.plot(mean_scores, label='Mean Score', color='red')
    plt.legend(loc='upper left')
    plt.ylim(ymin=0)
    # plt.xlim(xmin=0)
    plt.text(len(scores) - 1, scores[-1],str(scores[-1]), color='blue', fontsize=12, ha='right')
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]), color='red', fontsize=12, ha='right')
    # plt.show()