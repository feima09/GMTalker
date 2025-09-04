import gradio as gr

import utils.config as config


def create_ui(*args):
    with gr.Column():
        audio2face_config = config.Webui.get('audio2face', {})
        audio2face_enabled = gr.Checkbox(
            value=audio2face_config.get("enable", False),
            label="启用Audio2Face"
        )
        audio2face_path_input = gr.Textbox(
            value=audio2face_config.get("path", ""),
            label="Audio2Face路径",
            placeholder="请输入Audio2Face的路径",
            lines=1,
            max_lines=1,
            visible=audio2face_enabled.value,
            interactive=True
        )
        usd_path_input = gr.Textbox(
                value=audio2face_config.get("usd_path", ""),
                label="Audio2Face USD路径",
                placeholder="请输入Audio2Face的USD文件路径",
                lines=1,
                max_lines=1,
                visible=audio2face_enabled.value,
                interactive=True
            )

        audio2face_enabled.change(
            fn=lambda x: [gr.update(visible=x), gr.update(visible=x), gr.update(visible=x)],
            inputs=audio2face_enabled,
            outputs=[audio2face_path_input, usd_path_input, args[0]]
        )
    
    with gr.Column():
        ue5_config = config.Webui.get('ue5', {})
        ue5_enabled = gr.Checkbox(
            value=ue5_config.get("enable", False),
            label="启用UE5"
        )
        ue5_path_input = gr.Textbox(
            value=ue5_config.get("path", ""),
            label="UE5路径",
            placeholder="请输入UE5的exe路径",
            lines=1,
            max_lines=1,
            visible=ue5_enabled.value,
            interactive=True
        )
        
        ue5_enabled.change(
            fn=lambda x: [gr.update(visible=x), gr.update(visible=x)],
            inputs=ue5_enabled,
            outputs=[ue5_path_input, args[1]]
        )
        
    # 单一保存按钮
    save_button = gr.Button("保存所有配置", variant="primary", size="lg")
    save_output = gr.Textbox(label="保存结果")
    
    def save_config(*args):
        config.Webui["audio2face"] = {
            "enable": args[0],
            "path": args[1],
            "usd_path": args[2]
        }
        config.Webui["ue5"] = {
            "enable": args[3],
            "path": args[4]
        }
        config.save_config(config.Webui, "webui.yaml")
        return "配置已保存"

    save_button.click(
        fn=save_config,
        inputs=[audio2face_enabled, audio2face_path_input, usd_path_input, ue5_enabled, ue5_path_input],
        outputs=save_output
    )
    