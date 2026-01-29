export function getUserId() {
    let id = localStorage.getItem("anon_user");
    if (!id) {
        id = "user-" + Math.random().toString(36).substring(2, 10);
        localStorage.setItem("anon_user", id);
    }
    return id;
}
