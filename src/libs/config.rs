use std::collections::HashMap;

enum Value {
    Text(String),
    Bool(bool),
    Int(i64),
    Float(f64),
    Table(HashMap<String, Value>),
    List(Vec<Value>),
}

impl From<&str> for Value {
    fn from(s: &str) -> Value {
        return Self::Text(String::from(s));
    }
}

impl From<bool> for Value {
    fn from(b: bool) -> Value {
        return Self::Bool(b);
    }
}

impl TryFrom<&Value> for String {
    type Error = String;

    fn try_from(v: &Value) -> Result<String, Self::Error> {
        if let Value::Text(v) = v {
            return Ok(String::from(v));
        }
        return Err("Type mismatch".to_string());
    }
}

impl TryFrom<&Value> for bool {
    type Error = String;

    fn try_from(v: &Value) -> Result<bool, Self::Error> {
        if let Value::Bool(v) = v {
            return Ok(v.to_owned());
        }
        return Err("Type mismatch".to_string());
    }
}

pub struct Config {
    defaults: HashMap<String, Value>,
    locals: HashMap<String, Value>
}

impl Config {
    fn new() -> Self {
        Config {
            defaults: HashMap::new(),
            locals: HashMap::new(),
        }
    }

    fn set_default<K: AsRef<str>, V: Into<Value>>(&mut self, k: K, v: V) {
        self.defaults.insert(k.as_ref().to_string(), v.into());
    }

    // TODO: Why we has to set this lifetime
    fn get<'a, K: AsRef<str>, T: TryFrom<&'a Value, Error=String>>(&'a self, k: K) -> Result<T, String> {
        if let Some(v) = self.defaults.get(k.as_ref()) {
            return v.try_into();
        } else if let Some(v) = self.locals.get(k.as_ref()) {
            return v.try_into();
        }
        return Err(format!("Key {} not found", k.as_ref()));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_config() {
        let mut c = Config::new();
        c.set_default("a", "b");
        c.set_default("b", true);
        let v: String = c.get("a").unwrap();
        assert_eq!(v, "b");
        let v: bool = c.get("b").unwrap();
        assert!(v);
    }
}
