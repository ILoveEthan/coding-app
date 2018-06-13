import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import UsersList from '../UsersList';

const users = [
  {
    'active': true,
    'email': 'iamaprotoss@gmail.com',
    'id': 1,
    'username': 'zhenwei',
    'admin': false
  },
  {
    'acitve': true,
    'email': '178125918@qq.com',
    'id': 2,
    'username': 'ethan',
    'admin': false
  }
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  expect(wrapper.find('h1').get(0).props.children).toBe('All Users');
  const table = wrapper.find('Table');
  expect(table.length).toBe(1);
  expect(wrapper.find('thead').length).toBe(1);
  const th = wrapper.find('th');
  expect(th.length).toBe(5);
  expect(th.get(0).props.children).toBe('User ID');
  const td = wrapper.find('tbody > tr > td');
  expect(td.length).toBe(10);
  expect(td.get(0).props.children).toBe(1);
});

test('UsersList renders a snapshot properly', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});