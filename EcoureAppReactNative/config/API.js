import axios from "axios";

const baseURL='https://thanhduong.pythonanywhere.com/'
export const endpoint={
    'category':"/categories/",
    'course':"/courses/"
};
export default axios.create({
    baseURL:baseURL
})
