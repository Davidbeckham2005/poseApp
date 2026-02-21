// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use serde::{Deserialize, Serialize};
#[derive(Serialize, Deserialize)]
struct PyRequest{
    exercise: String,
    src: String, 
}
#[tauri::command]
fn call_python(payload: PyRequest) -> String {
    use std::process::Command;

    let arg = serde_json::to_string(&payload).unwrap();  
    let output = Command::new("python")
        .arg("python/main.py")
        .arg(arg)
        .output()
        .expect("failed to run python");
    
    String::from_utf8_lossy(&output.stdout).to_string()
}



#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![call_python])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
