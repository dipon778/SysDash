// ui/cpu.rs
use ratatui::{
    widgets::{Block, Borders, Sparkline},
    layout::Rect,
    Frame,
};

pub fn draw_cpu(frame: &mut Frame, area: Rect, cpu_usage: &[f32]) {
    let sparkline = Sparkline::default()
        .block(Block::default().title("CPU Usage").borders(Borders::ALL))
        .data(cpu_usage)
        .max(100);
    frame.render_widget(sparkline, area);
}