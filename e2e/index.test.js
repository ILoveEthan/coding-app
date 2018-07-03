import { Selector } from 'testcafe';
const TEST_URL = process.env.TEST_URL;
fixture('/').page(`${TEST_URL}/`);
test(`index '/' page is showing`, async (t) =>  {
  await t
    .navigateTo(TEST_URL)
    .expect(Selector('H1').withText('Exercises').exists).ok()
});