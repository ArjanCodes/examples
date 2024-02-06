// rustimport:pyo3

use pyo3::prelude::*;

#[pyclass]
#[derive(Debug, Clone, PartialEq)]
enum AttachmentType {
    Image,
    Video,
    Audio,
    File,
}

#[pyclass(module = "pyo3_rust", get_all, set_all)]
#[derive(Debug, Clone, PartialEq)]
struct Attachment {
    path: String,
    attachment_type: AttachmentType,
}

#[pymethods]
impl Attachment {
    #[new]
    fn new(path: String, attachment_type: AttachmentType) -> Self {
        Attachment {
            path,
            attachment_type,
        }
    }
    
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("Attachment(path={}, attachment_type={:?})", self.path, self.attachment_type))
    }
}

#[pyclass(module = "pyo3_rust", get_all, set_all)]
#[derive(Debug, Clone)]
struct Email {
    subject: String,
    body: String,
    attachments: Vec<Attachment>,
}

#[pymethods]
impl Email {
    #[new]
    fn new(subject: String, body: String, attachments: Vec<Attachment>) -> Self {
        Email {
            subject,
            body,
            attachments,
        }
    }
    
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("Email(subject={}, body={}, attachments={:?})", self.subject, self.body, self.attachments))
    }
    
    fn send(&mut self, to: String) -> PyResult<()> {
        println!("Sending email to: {}", to);
        println!("Subject: {}", self.subject);
        println!("Body: {}", self.body);
        for attachment in &self.attachments {
            println!("Attachment: {:?}", attachment);
        }
        Ok(())
    }
    
}

#[pymodule]
fn pyo3_rust_simple(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Attachment>()?;
    m.add_class::<Email>()?;
    m.add_class::<AttachmentType>()?;
    Ok(())
}

