import { Selector } from 'testcafe';

const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;


const TEST_URL = process.env.TEST_URL;
fixture('/register').page(`${TEST_URL}/register`);
test(`registration form '/register' is showing`, async (t) => {
  await t
    .navigateTo(`${TEST_URL}/register`)
    .expect(Selector('H1').withText('Register').exists).ok()
    .expect(Selector('form').exists).ok()
});

test(`a user is able to register`, async (t) => {
  await t
    .navigateTo(`${TEST_URL}/register`)
    .typeText('input[name="username"]', username)
    .typeText('input[name="email"]', email)
    .typeText('input[name="password"]', 'randomrandom')
    .click(Selector('input[type="submit"]'))

  await t
    .expect(Selector('button').withText('Run Code').exists).ok()
    .expect(Selector('a').withText('User Status').exists).ok()
    .expect(Selector('a').withText('Log Out').exists).ok()
    .expect(Selector('a').withText('Register').exists).notOk()
    .expect(Selector('a').withText('Log In').exists).notOk()

});