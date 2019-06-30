# -*- coding: utf-8 -*-
from backend.api.abstract import ActionApi
from backend.views.abstract import parse_arguments, check_request_method, current_user_anonymous
from flask.ext.restful.reqparse import Argument
from flask.ext.login import login_user, logout_user
import ast
import random
from backend import cache
from flask import session, current_app, redirect
from backend.models import User, WorkOrder
from backend.models.user import load_user
from backend.models.company import Company
from flask.ext.login import current_user
from backend.core.send_message import core_send_message
from bson import ObjectId
from Crypto.Util.number import getRandomNBitInteger


class UserApi(ActionApi):
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('username', type=int, required=True),
        Argument('password', type=str, required=True),
    )
    def login(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/login 用户登录
        @apiName login
        @apiGroup User

        @apiParam {int} username 用户手机号作为登录用户名
        @apiParam {String} password 用户密码

        @apiSuccess {String} message y验证结果
        """
        mobile = arguments['username']
        password = arguments['password']
        user = User.user_find_one({'mobile': mobile})
        if not user:
            return self.fail(message=u'该用户名不存在')
        if user.validate_login(user['password'], password):
            user = load_user(user['uid'])
            login_user(user, remember=True)
            return self.done({'current_user': user})
        else:
            return self.fail(message=u'密码不正确')

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('code', type=int, required=True),
    )
    def new_login(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/new_login 用户登录(new)
        @apiName new_login
        @apiGroup User

        @apiParam {int} mobile 用户手机号作为登录用户名
        @apiParam {int} code 用户密码

        @apiSuccess {String} message y验证结果
        """
        mobile = arguments['mobile']
        verify_code = arguments['code']
        user = User.find_one({'mobile': mobile})
        if not user:
            return self.fail(message=u'该用户不存在')
        if verify_code != int(session[str(mobile)]):
            return self.fail(message=u'验证码不正确')
        if user.get('company_id') and len(user['company_id']) != 0:
            user = load_user(user['uid'])
            login_user(user, remember=True)
            return self.done(User.user_find_one({'mobile': mobile}))
        else:
            return self.fail(u"用户没有公司,请先创建公司")

    @current_user_anonymous()
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('cId', type=str, required=False)
    )
    def set_company(self, arguments):
        """
        设置session的companyId
        """
        company_id = current_user['company_id'][0]
        if arguments['cId'] and Company.find_one({'company_id': int(arguments['cId'])}):
            company_id = arguments['cId']
        session["current_company"] = company_id
        session["current_user_company"] = Company.company_find_one({'company_id': int(company_id)})
        return self.done(company_id)

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True)
    )
    def get_verify_code(self, arguments):
        r = str(getRandomNBitInteger(128))
        if current_app.config['DEBUG']:
            verify_code = '111111'
        else:
            # verify_code = str(random.random())[2:8]
            verify_code = r[2:8]

        session[str(arguments['mobile'])] = verify_code
        if current_app.config['DEBUG']:
            return self.done("success")
        else:
            core_send_message(str(arguments['mobile']), {'code': verify_code}, 'zljVerifyCode')
            return self.done("success")

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('verify_code', type=int, required=True),
        Argument('password', type=str, required=True),
        Argument('company_name', type=str, required=True)
    )
    def register(self, arguments):
        mobile = arguments['mobile']
        if User.find_one({'mobile': mobile}):
            return self.fail(message=u"该手机号码已注册")
        password = arguments['password']
        company_name = arguments['company_name']
        verify_code = arguments['verify_code']
        if verify_code != int(session[str(mobile)]):
            return self.fail(message=u'验证码不正确')
        company = Company.find_one({'company_name': company_name})
        if company:
            company_id = company['company_id']
        else:
            new_company = Company.create_company(company_name)
            company_id = new_company['company_id']
        for item in ['mobile', 'verify_code', 'password', 'company_name']:
            del arguments[item]
        user = User.create_user(int(mobile), password, company_id, **arguments)
        user = load_user(user['uid'])
        login_user(user, remember=True)
        del user['password']
        return self.done(data=user)

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('company_name', type=unicode, required=True),
        Argument('company_address', type=unicode, required=True),
        Argument('contact_person', type=unicode, required=True),
        Argument('mobile', type=int, required=True),
    )
    def submit_info(self, arguments):
        if WorkOrder.find_one({'mobile': int(arguments['mobile'])}):
            return self.fail(message=u"该手机号码已被使用")
        result = WorkOrder.create(**arguments)
        return self.done('success') if result else self.fail('fail')

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('code', type=int, required=True)
    )
    def invite(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/invite 邀请用户的公司列表
        @apiName invite
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        """
        mobile = arguments['mobile']
        verify_code = arguments['code']
        if verify_code != int(session[str(mobile)]):
            return self.fail(message=u'验证码不正确')
        # 找到所以 "invite" : [ { "12333" : 18702156534} , { "324" : 18702156534}] 里面的324的数据
        query = {'invite': {'$elemMatch': {str(mobile): {'$exists': True}}}}
        result = Company.find(query)
        total = result.count()
        return self.done({
            'items': [Company.as_dict(item) for item in result],
            'total': total
        })

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('company_name', type=str, required=True)
    )
    def new_register(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/new_register 新的注册接口
        @apiName new_register
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        @apiParam {int} company_name 公司名称
        """
        mobile = arguments['mobile']
        if User.find_one({'mobile': mobile}):
            return self.fail(message=u"该手机号码已注册")
        password = str(mobile)
        company_name = arguments['company_name']
        company = Company.find_one({'company_name': company_name})
        if company:
            return self.fail(message=u"该公司已存在")
        else:
            new_company = Company.create_company(company_name)
            company_id = new_company['company_id']
        for item in ['mobile', 'company_name']:
            del arguments[item]
        user = User.create_user(int(mobile), password, [company_id], **arguments)
        Company.update_one({'_id': new_company['_id']}, {'$set': {'admin': user['uid']}})
        permission = {str(company_id): {'shouzu': '允许', 'zhaozu': '允许'}}
        User.update_one({'uid': user['uid']}, {'$set': {'permission': permission}})
        user = load_user(user['uid'])
        login_user(user, remember=True)
        session["current_company"] = company_id
        session["current_user_company"] = Company.company_find_one({'company_id': int(company_id)})
        return self.done("success")

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('company_name', type=str, required=True)
    )
    def disable_register(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/disable_register 被禁用户的注册接口
        @apiName disable_register
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        @apiParam {int} company_name 公司名称
        """
        company_name = arguments['company_name']
        mobile = arguments['mobile']
        user = User.find_one({'mobile': mobile})
        company = Company.find_one({'company_name': company_name})
        if company:
            return self.fail(message=u"该公司已存在")
        else:
            params = {'admin': user['uid']}
            company = Company.create_company(company_name, **params)
            user['company_id'].append(company['company_id'])
            result = User.update_one({'_id': user['_id']},
                                     {'$set': {'company_id': user['company_id']}})
            if result.raw_result['ok'] == 1:
                user = load_user(user['uid'])
                login_user(user, remember=True)
                return self.done(u"登录成功")
            else:
                return self.fail(u"添加失败")

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('company_id', type=str, required=True)
    )
    def disable_user_invited(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/disable_user_invited 被禁用户接受邀请
        @apiName disable_user_invited
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        @apiParam {int} company_id 公司id
        """
        mobile = arguments['mobile']
        user_result = User.find_one({'mobile': int(mobile)})
        company_list = ast.literal_eval(arguments['company_id'])
        if not user_result:
            return self.fail(u"该手机号码不存在")
        if not company_list:
            return self.fail(u"公司不存在")
        for i in company_list:
            company = Company.find_one({'company_id': int(i)})
            invite_list = []
            for j in company['invite']:
                if str(mobile) not in j:
                    invite_list.append(j)
                else:
                    permission = j[str(mobile)].get('permission')
                    if not user_result['permission']:
                        user_result['permission'] = {}
                    user_result['permission'][str(i)] = permission
            if int(i) not in user_result['company_id']:
                user_result['company_id'].append(int(i))
            User.update_one({'uid': user_result['uid']},
                            {'$set': {'company_id': user_result['company_id'],
                                      'permission': user_result['permission']}})
            use_list = company.get('use') if company.get('use') else []
            use_list.append(user_result['uid'])
            Company.update_one({'_id': company['_id']},
                               {'$set': {'invite': invite_list, 'use': use_list}})
            user = load_user(user_result['uid'])
            login_user(user, remember=True)
        return self.done()

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('company_id', type=unicode, required=True)
    )
    def add_company(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/add_company 用户注册并添加新的公司
        @apiName add_company
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        @apiParam {int} company_id 公司id
        """
        mobile = arguments['mobile']
        if User.find_one({'mobile': mobile}):
            return self.fail(message=u"该手机号码已注册")
        password = str(mobile)
        company_list = ast.literal_eval(arguments['company_id'])
        permission = {}
        for i in company_list:
            company = Company.find_one({'company_id': int(i)})
            invite_list = []
            for j in company['invite']:
                if str(mobile) not in j:
                    invite_list.append(j)
                else:
                    permission[str(i)] = j[str(mobile)].get('permission')
            company['invite'] = invite_list
            Company.update_one({'_id': company['_id']}, {'$set': company})
        user = User.create_user(int(mobile), password, company_list)
        user.update_one({'_id': user['_id']}, {'$set': {'permission': permission}})
        user = load_user(user['uid'])
        for i in company_list:
            company = Company.find_one({'company_id': int(i)})
            use_list = company.get('use') if company.get('use') else []
            use_list.append(user['uid'])
            company['use'] = use_list
            Company.update_one({'_id': company['_id']}, {'$set': company})
        login_user(user, remember=True)
        return self.done()

    @current_user_anonymous()
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('company_id', type=str, required=True)
    )
    def user_add_company(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/user_add_company 添加新的公司
        @apiName user_add_company
        @apiGroup User

        @apiParam {int} mobile 用户手机号
        @apiParam {int} company_id 公司id
        """
        mobile = arguments['mobile']
        company_id = arguments['company_id']
        user_result = User.find_one({'mobile': int(mobile)})
        company_result = Company.find_one({'company_id': int(company_id)})
        if not user_result:
            return self.fail(u"该手机号码不存在")
        if not company_result:
            return self.fail(u"公司不存在")
        if int(company_id) not in user_result['company_id']:
            user_result['company_id'].append(int(company_id))
        invite_list = []
        for j in company_result['invite']:
            if str(mobile) not in j:
                invite_list.append(j)
            else:
                permission = j[str(mobile)].get('permission')
                if not user_result['permission']:
                    user_result['permission'] = {}
                user_result['permission'][str(company_id)] = permission
        User.update_one({'uid': user_result['uid']},
                        {'$set': {'company_id': user_result['company_id'], 'permission': user_result['permission']}})
        if not company_result.get('use'):
            company_result['use'] = []
        company_result['use'].append(user_result['uid'])
        Company.update_one({'_id': company_result['_id']},
                           {'$set': {'invite': invite_list, 'use': company_result['use']}})
        return self.done()

    @current_user_anonymous()
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('name', type=str, required=True)
    )
    def create_company(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/create_company 用户创建公司
        @apiName create_company
        @apiGroup User

        @apiParam {str} name 公司名称
        """
        new_company = arguments['name']
        company = Company.find_one({'company_name': new_company})
        if company:
            return self.fail(u"公司名已存在")
        else:
            # params = {'use': [current_user['uid']]}
            company = Company.create_company(new_company)
            user = current_user
            user['company_id'].append(company['company_id'])
            result = User.update_one({'_id': user['_id']},
                                     {'$set': {'company_id': user['company_id']}})
            if result.raw_result['ok'] == 1:
                return self.done(u"添加成功")
            else:
                return self.fail(u"添加失败")

    @current_user_anonymous()
    @check_request_method(['GET'])
    def company_list(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/V1/user/company_list 用户公司列表
        @apiName company_list
        @apiGroup User
        """
        items = []
        for i in xrange(len(current_user['company_id'])):
            company_id = current_user['company_id'][i]
            company_name = (Company.find_one({'company_id': company_id}))['company_name']
            items.append({company_id: company_name})

        query = {'invite': {'$elemMatch': {str(current_user['mobile']): {'$exists': True}}}}
        invite_list = Company.find(query)
        return self.done({
            'items': items,
            'invite': [Company.as_dict(item) for item in invite_list],
            'uid': current_user['uid']
        })

    @current_user_anonymous()
    @check_request_method(['GET'])
    def current_user(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/V1/user/current_user 用户个人信息
        @apiName current_user
        @apiGroup User
        """
        from backend.core.aes_crypt import encrypt
        # text = "This is for test."
        # en_data = encrypt(data=text)
        user = User.as_dict(current_user)
        for i in ['password', 'ctime', 'utime']:
            del user[i]
        # user['en_data'] = en_data
        return self.done(user)

    @current_user_anonymous()
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True),
        Argument('code', type=int, required=True)
    )
    def edit_mobile(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/edit_mobile 更新用户手机号码
        @apiName edit_mobile
        @apiGroup User

        @apiParam {str} name 公司名称
        """
        mobile = arguments['mobile']
        verify_code = arguments['code']
        if verify_code != int(session[str(mobile)]):
            return self.fail(message=u'验证码不正确')
        if User.find_one({'mobile': mobile}):
            return self.fail(u"此手机已经被注册过了")
        result = User.update_one({'_id': current_user['_id']}, {'$set': {'mobile': mobile}})
        if result.raw_result['ok'] == 1:
            return self.done("success")
        else:
            return self.fail(u"更新失败")

    @current_user_anonymous()
    @check_request_method(['POST'])
    @parse_arguments(
        Argument('name', type=str, required=False),
        Argument('user_img', type=str, required=False)
    )
    def edit(self, arguments):
        """
        @apiVersion 1.0.0
        @api {post} /api/V1/user/edit 更新用户信息
        @apiName edit
        @apiGroup User

        @apiParam {str} name 公司名称
        """
        name = arguments['name']
        img_url = arguments['user_img']
        renew = {}
        if name:
            renew['name'] = name
        if img_url:
            renew['user_img'] = img_url
        result = User.update_one({'_id': current_user['_id']}, {'$set': renew})
        if result.raw_result['ok'] == 1:
            return self.done(User.user_find_one({'_id': current_user['_id']}))
        else:
            return self.fail(u"更新失败")

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('oid', type=str, required=True),
        Argument('company_id', type=str, required=True),
        Argument('menu', type=str, required=True),
        Argument('checked', type=str, required=True)
    )
    def change_permission(self, arguments):
        user = User.find_by_id(arguments['oid'])
        if user.get('permission'):
            permission = user.get('permission')
            if permission.get(arguments['company_id']):
                permission[arguments['company_id']][arguments['menu']] = arguments['checked']
        else:
            permission = {arguments['company_id']: {'shouzu': '允许', 'zhaozu': '允许'}}

        User.update_one({'_id': ObjectId(arguments['oid'])}, {'$set': {'permission': permission}})

    @current_user_anonymous()
    @check_request_method(['GET'])
    def current_user_bind_58(self):
        """
        @apiVersion 1.0.0
        @api {get} /api/V1/user/current_user_bind_58 当前用户是否绑定58同城
        @apiName current_user_bind_58
        @apiGroup User
        """
        company = current_user['company_id'][0]
        account_58 = Company.find({'company_id': company})[0]['account']
        password_58 = Company.find({'company_id': company})[0]['password']
        bind_58_state = False
        if account_58 and password_58:
            bind_58_state = True
        return self.done({
            "bind_58_state": bind_58_state,
        })

    @check_request_method(['POST'])
    @parse_arguments(
        Argument('mobile', type=int, required=True)
    )
    def exist_user(self, arguments):
        mobile = arguments['mobile']
        if User.find_one({'mobile': mobile}):
            return self.fail(u"用户已存在")
        else:
            return self.done(u"用户不存在")

    @current_user_anonymous()
    @check_request_method(['POST'])
    def logout_current_user(self):
        user_info = User.user_find_one({'uid': current_user['uid']})
        logout_user()
        session.pop('current_company', None)
        session.pop('current_user_company', None)
        return self.done({'uid': user_info['uid']})
