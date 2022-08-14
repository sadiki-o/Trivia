# Quizzio frontend



This is the frontend of the Quizzio game, made with **React** & **Typescript** & **Tailwindcss** & **Zustand**



### Project structure

|___ Trivia

​    |___ .env

​    |___ index.html

​    |___ package.json

​    |___ postcss.config.cjs

​    |___ tailwind.config.cjs

​    |___ tsconfig.json

​    |___ tsconfig.node.json

​    |___ vite.config.ts

​    |___ yarn-error.log

​    |___ yarn.lock

​    |___ public

​        |___ question.png

​    |___ src

​        |___ App.css

​        |___ App.tsx

​        |___ index.css

​        |___ main.tsx

​        |___ vite-env.d.ts

​        |___ assets

​        |___ components

​        |___ utils

​        |___ zustandStore

### Install dependencies

in order to setup the frontend, do the following after you cd into the <u>frontend</u> directory :

```
yarn add
```

or :

```
npm install
```

in order to install the required packages

### Scripts 

```json
"scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
```

to run :

`yarn dev` or `yarn vite`

and then visit the port your application is setup for, in my case <u>5173</u>



### Project description

The game lets you create an account or signup a new one, by default there is an **admin** account with the following credentials:

`username: admin `  `password: adminadmin`

You can create your own categories and questions, as well as exploring the system categories and questions, you can play by choosing a category or play with all questions, get your score at the end of each round.

