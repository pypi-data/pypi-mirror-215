use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::wrap_pymodule;

// #[pyfunction]
// fn create_input(simulation_id: String, sub_command: String, arguments: Vec<String>, prompts: Vec<String>, files_input: Vec<String>, files_output: Vec<String>) -> PyResult<String> {
//     let input = chiral_common::app::chem::gromacs::gmx_command::Input { simulation_id, sub_command, arguments, prompts, files_input, files_output};
//     Ok(input.ser_to())
// }

/// A Python module implemented in Rust.
#[pymodule]
fn chiral_bindings(py: Python, m: &PyModule) -> PyResult<()> {
    // m.add_function(wrap_pyfunction!(create_input, m)?)?;
    m.add_wrapped(wrap_pymodule!(chiral_common::app::chem::gromacs::gmx_command::gromacs_gmx_command))?;
    m.add_wrapped(wrap_pymodule!(chiral_common::job::job_module))?;

    let sys = PyModule::import(py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    sys_modules.set_item("chiral_bindings.gromacs_gmx_command", m.getattr("gromacs_gmx_command")?)?;
    sys_modules.set_item("chiral_bindings.job_module", m.getattr("job_module")?)?;

    Ok(())
}