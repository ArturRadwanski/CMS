import { writable } from "svelte/store";

export const loggedIn = writable(false);
export const admin = writable(false);
export const contentEditMode = writable(false);
export const nickname = writable("");
export const articles = writable([]);
export const stylesEditMode = writable(false);
export const stylesSt = writable([])
export const burger = writable(false)
export const ord = writable(0)