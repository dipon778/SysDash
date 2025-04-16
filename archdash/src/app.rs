// app.rs
use sysinfo::{System, SystemExt};
use anyhow::Result;

pub struct App {
    sys: System,
    cpu_usage: Vec<f32>,
    memory_used: u64,
    memory_total: u64,
    swap_used: u64,
    swap_total: u64,
    // Add more fields as needed
}

impl App {
    pub fn new() -> Self {
        let mut sys = System::new_all();
        sys.refresh_all();
        
        Self {
            sys,
            cpu_usage: Vec::new(),
            memory_used: 0,
            memory_total: 0,
            swap_used: 0,
            swap_total: 0,
        }
    }
    
    pub fn update(&mut self) -> Result<()> {
        self.sys.refresh_all();
        self.cpu_usage = self.sys.cpus().iter()
            .map(|cpu| cpu.cpu_usage())
            .collect();
        self.memory_used = self.sys.used_memory();
        self.memory_total = self.sys.total_memory();
        self.swap_used = self.sys.used_swap();
        self.swap_total = self.sys.total_swap();
        Ok(())
    }
}