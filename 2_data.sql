SET client_encoding TO 'GBK';

DELETE FROM sys_user;
DELETE FROM passwords;

INSERT INTO sys_user (user_sn, user_name) VALUES
    (101, 'zhangsan'),
    (102, 'lisi'),
    (103, 'wangwu'),
    (104, 'maliu');

INSERT INTO passwords (user_sn, password) VALUES
    (101, '123'),
    (102, '456'),
    (103, '789'),
    (104, '000');

    hashed = principal.get("password")
    print(f"未哈希的密码表的密码={hashed}")
    """salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(principal.get("password").encode("utf-8"), salt).decode("utf-8")
    print(f"哈希后的密码表的密码={hashed}")
    result = bcrypt.checkpw(principal.get("password").encode("utf-8"), hashed.encode("utf-8"))
    print(f"结果={result}")"""