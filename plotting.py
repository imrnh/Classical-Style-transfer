import os
import matplotlib.pyplot as plt
from utils import get_stylized_rgb

def plot_and_save(stylized_images, content_images, style_images):
    fig, axs = plt.subplots(len(stylized_images), 3, figsize=(11, 10))

    # Naming columns
    if len(stylized_images) > 1:
        axs[0, 0].set_title("Original Image")
        axs[0, 1].set_title("Style Image")
        axs[0, 2].set_title("Transferred Image")
    else:
        axs[0].set_title("Original Image")
        axs[1].set_title("Style Image")
        axs[2].set_title("Transferred Image")

    for i in range(len(stylized_images)):
        if len(stylized_images) > 1:
            axs[i, 0].imshow(content_images[i])
            axs[i, 1].imshow(style_images[i])
            axs[i, 2].imshow(get_stylized_rgb(stylized_images[i]))

            # Turning off axis coords
            axs[i, 0].axis("off")
            axs[i, 1].axis("off")
            axs[i, 2].axis("off")

        else:
            axs[0].imshow(content_images[i])
            axs[1].imshow(style_images[i])
            axs[2].imshow(get_stylized_rgb(stylized_images[i]))

            # Turning off axis coords
            axs[0].axis("off")
            axs[1].axis("off")
            axs[2].axis("off")

    plt.axis('off')
    plt.tight_layout()
    plt.savefig("output.png")
    plt.show()



def save_stylized_outputs(stylized_images, content_images, style_images, output_dir="images/output"):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(stylized_images)):
        fig, axs = plt.subplots(1, 3, figsize=(11, 4))

        axs[0].imshow(content_images[i])
        axs[1].imshow(style_images[i])
        axs[2].imshow(get_stylized_rgb(stylized_images[i]))

        axs[0].set_title("Original Image")
        axs[1].set_title("Style Image")
        axs[2].set_title("Transferred Image")

        for ax in axs:
            ax.axis("off")

        plt.tight_layout()
        save_path = os.path.join(output_dir, f"{i+1}.png")
        plt.savefig(save_path)
        plt.close(fig)


def plot_for_streamlit(stylized_images, content_images, style_images):
    fig, axs = plt.subplots(len(stylized_images), 3, figsize=(11, 15))

    # Naming columns
    if len(stylized_images) > 1:
        axs[0, 0].set_title("Original Image")
        axs[0, 1].set_title("Style Image")
        axs[0, 2].set_title("Transferred Image")
    else:
        axs[0].set_title("Original Image")
        axs[1].set_title("Style Image")
        axs[2].set_title("Transferred Image")

    for i in range(len(stylized_images)):
        if len(stylized_images) > 1:
            axs[i, 0].imshow(content_images[i])
            axs[i, 1].imshow(style_images[i])
            axs[i, 2].imshow(get_stylized_rgb(stylized_images[i]))

            axs[i, 0].axis("off")
            axs[i, 1].axis("off")
            axs[i, 2].axis("off")
        else:
            axs[0].imshow(content_images[i])
            axs[1].imshow(style_images[i])
            axs[2].imshow(get_stylized_rgb(stylized_images[i]))

            axs[0].axis("off")
            axs[1].axis("off")
            axs[2].axis("off")

    plt.tight_layout()
    return fig
