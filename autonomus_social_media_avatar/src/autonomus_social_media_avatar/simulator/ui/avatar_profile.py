import gradio as gr
import matplotlib.pyplot as plt
import numpy as np

def create_avatar_profile():
    gr.Markdown("### Avatar's Profile")
    with gr.Row():
        sliders = [
            gr.Slider(0, 1, step=0.1, label=f"Skill {i+1}") for i in range(6)
        ]
    submit_btn = gr.Button("Generate Plot")
    output_image = gr.Image()

    submit_btn.click(create_hexagonal_plot, sliders, output_image)


def create_hexagonal_plot(*skill_values):
    labels = ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5", "Skill 6"]
    num_vars = len(labels)

    # Ensure the data wraps around to close the radar plot
    values = list(skill_values) + [skill_values[0]]

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Plot setup
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Adjust based on your scale
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Save the figure to return
    plt.tight_layout()
    fig_path = "radar_chart.png"
    plt.savefig(fig_path)
    plt.close(fig)
    return fig_path