macro_rules! impl_iot_device {
    ($type:ty) => {
        impl IOTDevice for $type {
            fn connect(&mut self) {
                self.connection.connect("Arjan", "localhost", 8080);
            }

            fn disconnect(&mut self) {
                self.connection.disconnect();
            }

            fn send(&mut self, message: &str) {
                self.connection.send(message);
            }

            fn receive(&mut self) -> Option<String> {
                self.connection.receive()
            }
        }
    };
}
#[derive(Debug, Default)]
enum ConnectionStatus {
    Connected{ name: String, ip: String, port: u16 },
    #[default]
    Disconnected,
}

impl ConnectionStatus {
    fn new(name: String, ip: String, port: u16) -> ConnectionStatus {
        ConnectionStatus::Connected{ name, ip, port }
    }

    fn connect(&mut self, name: String, ip: String, port: u16) {
        *self = ConnectionStatus::Connected{ name, ip, port };
    }

    fn disconnect(&mut self) {
        *self = ConnectionStatus::Disconnected;
    }

    fn send(&self, message: &str) {
        match self {
            ConnectionStatus::Connected{ name, ip, port } => {
                println!("Sent {} to {} at {}:{}", message, name, ip, port);
            },
            ConnectionStatus::Disconnected => {
                println!("Cannot send message, not connected");
            },
        }
    }

    fn receive(&self) -> Option<String> {
        if let ConnectionStatus::Connected{ name, ip, port } = self {
            Some(format!("Received message from {} at {}:{}", name, ip, port))
        } else {
            None
        }
    }
}
trait IOTDevice {
    fn connect(&mut self);
    fn disconnect(&mut self);
    fn send(&mut self, message: &str);
    fn receive(&mut self) -> Option<String>;
}

struct Light {
    connection: ConnectionStatus,
}

impl IOTDevice for Light {
    fn connect(&mut self) {
        self.connection.connect("Arjan".to_string(), "localhost".to_string(), 8080);
    }

    fn disconnect(&mut self) {
        self.connection.disconnect();
    }

    fn send(&mut self, message: &str) {
        self.connection.send(message);
    }

    fn receive(&mut self) -> Option<String> {
        self.connection.receive()
    }
}

// impl_iot_device!(Light); // this macro can be used instead of the above impl IOTDevice for Light


impl Light {
    fn new() -> Light {
        Light {
            connection: ConnectionStatus::default(),
        }
    }
}


fn main() {
    let mut light = Light::new();
    light.connect();
    light.send("Hello");
    light.disconnect();
    println!("{:?}", light.receive());
}