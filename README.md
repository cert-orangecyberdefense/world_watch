<p>World Watch advisories now can be retrieved using a dedicated REST API, located here: https://api-ww.cert.orangecyberdefense.com.
	
A Swagger is available publicly for your development tests, with the corresponding JSON here: https://api-ww.cert.orangecyberdefense.com/api/openapi.json

If you need an account on this API, please contact us at worldwatch-request.ocd@orange.com</p>


<h1>Permissions</h1>
<h2>Keys</h2>
<p>There are three types of keys:</p>
<ul>
<li>
<p>EmailKeyAuthentication</p></li>
<li>
<p>LoginTokenAuthentication</p></li>
<li>
<p>APIKeyAuthentication</p></li></ul>
<p>Different endpoints use different keys, and one user can have multiple keys at the same time.</p>
<p>You can know which endpoint uses which key by checking the <a href="https://worldwatch.atlassian.net/wiki/spaces/~557058f39668e7b5934f2fb9bbf5a2aa299248/pages/316538881/API-WW#Endpoints">endpoints</a> section.</p>
<h2>User Role</h2>
<p>There are four roles that a user can have:</p>
<ul>
<li>
<p>Admin</p></li>
<li>
<p>Manager</p></li>
<li>
<p>User</p></li>
<li>
<p>Analyst</p></li></ul>
<p>Different endpoints require different roles, and each user can have at most one role.</p>
<p>You can know which endpoint needs which user role by checking the <a href="https://worldwatch.atlassian.net/wiki/spaces/~557058f39668e7b5934f2fb9bbf5a2aa299248/pages/316538881/API-WW#Endpoints">endpoints</a> section.</p>
<h1>User Management</h1>
<p>In order to add a new user, you need:</p>
<ul>
<li>
<p>Be a user with a role of <strong>Manager</strong> or <strong>Admin</strong> </p></li>
<li>
<p>Be authenticated with a <strong>LoginTokenAuthentication</strong></p></li></ul>
<p>You will need to:</p>
<ol start="1">
<li>
<p>While authenticated, call the <code>/api/users [POST]</code> endpoint. It will return a user instance with an <strong>id</strong></p></li>
<li>
<p>While authenticated, call the<code> /api/users/{user_id}/send_invitation [POST]</code> endpoint. The user will receive an email with their <strong>EmailKeyAuthentication</strong>. </p></li>
<li>
<p>The user should use his <strong>EmailKeyAuthentication</strong> and call the <code>/api/users/validate [POST]</code> endpoint with his password.</p></li>
<li>
<p>If everything works correctly, the user should be able to login using the <code>/api/users/login [POST]</code> endpoint. This will return a <strong>LoginTokenAuthentication</strong></p></li></ol>
<p />
<p>In order to get an <strong>APIKeyAuthentication</strong>, you need to call the  <code>/api/api_keys [POST]</code> endpoint while authenticated.</p>
<h1>Models</h1>
<h2>Users</h2>
<h3>Table: <code>Users</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="ce3de52a-6d92-434b-bd25-88dc44aae7f3">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id            </p></td>
<td>
<p>integer  </p></td>
<td>
<p>                                             </p></td></tr>
<tr>
<td>
<p>email         </p></td>
<td>
<p>string   </p></td>
<td>
<p>unique, max_length=100, required             </p></td></tr>
<tr>
<td>
<p>username      </p></td>
<td>
<p>string   </p></td>
<td>
<p>auto_add (set to email value when creating record) </p></td></tr>
<tr>
<td>
<p>password      </p></td>
<td>
<p>string   </p></td>
<td>
<p>hashed, required                             </p></td></tr>
<tr>
<td>
<p>first_name    </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=50, required                      </p></td></tr>
<tr>
<td>
<p>last_name     </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=50, required                      </p></td></tr>
<tr>
<td>
<p>last_login    </p></td>
<td>
<p>datetime </p></td>
<td>
<p>auto_add                                     </p></td></tr>
<tr>
<td>
<p>is_active     </p></td>
<td>
<p>boolean  </p></td>
<td>
<p>True/False, not active can&rsquo;t login           </p></td></tr>
<tr>
<td>
<p>date_joined   </p></td>
<td>
<p>datetime </p></td>
<td>
<p>auto_add                                     </p></td></tr>
<tr>
<td>
<p>phone_number  </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=16, optional                      </p></td></tr>
<tr>
<td>
<p>company       </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=100, optional                     </p></td></tr>
<tr>
<td>
<p>department    </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=50, optional                      </p></td></tr>
<tr>
<td>
<p>country       </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=50, optional                      </p></td></tr>
<tr>
<td>
<p>verified      </p></td>
<td>
<p>boolean  </p></td>
<td>
<p>default is False                             </p></td></tr>
<tr>
<td>
<p>active_until  </p></td>
<td>
<p>datetime </p></td>
<td>
<p>optional                                     </p></td></tr>
<tr>
<td>
<p>role          </p></td>
<td>
<p>string   </p></td>
<td>
<p>choices=[admin, manager, user, analyst], default=user </p></td></tr></tbody></table>
<h3>Table: <code>Tokens</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="00aad442-88b7-4403-a769-b9ef04244ed6">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id         </p></td>
<td>
<p>integer  </p></td>
<td>
<p>                                       </p></td></tr>
<tr>
<td>
<p>name       </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=64, optional                </p></td></tr>
<tr>
<td>
<p>user_id    </p></td>
<td>
<p>integer  </p></td>
<td>
<p>not null</p></td></tr>
<tr>
<td>
<p>key        </p></td>
<td>
<p>string   </p></td>
<td>
<p>max_length=64, unique, auto-generated</p></td></tr>
<tr>
<td>
<p>expiration </p></td>
<td>
<p>datetime </p></td>
<td>
<p>default=default_login_key_expiration</p></td></tr>
<tr>
<td>
<p>type       </p></td>
<td>
<p>string   </p></td>
<td>
<p>choices=[auth, api_key, email_key]</p></td></tr>
<tr>
<td>
<p>revoked    </p></td>
<td>
<p>boolean  </p></td>
<td>
<p>default is False                       </p></td></tr></tbody></table>
<h2>Content</h2>
<h3>Table: <code>Threat Categories</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="14e19be1-01a3-4ea7-ac5a-bf656ab18def">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id       </p></td>
<td>
<p>integer</p></td>
<td>
<p>                      </p></td></tr>
<tr>
<td>
<p>title    </p></td>
<td>
<p>string </p></td>
<td>
<p>max_length=50, unique </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Tags</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="c66c586d-8cba-423d-a36a-9c861e780943">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id       </p></td>
<td>
<p>integer</p></td>
<td>
<p>                       </p></td></tr>
<tr>
<td>
<p>name     </p></td>
<td>
<p>string </p></td>
<td>
<p>max_length=100, unique </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Advisories</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="51788273-b12f-4321-a0b6-1c3851fd3ac2">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id                  </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                           </p></td></tr>
<tr>
<td>
<p>tdc_id              </p></td>
<td>
<p>integer       </p></td>
<td>
<p>null=True, blank=True      </p></td></tr>
<tr>
<td>
<p>title               </p></td>
<td>
<p>string        </p></td>
<td>
<p>max_length=200             </p></td></tr>
<tr>
<td>
<p>severity            </p></td>
<td>
<p>integer       </p></td>
<td>
<p>allowed_range [0, 5]                     </p></td></tr>
<tr>
<td>
<p>threat_category     </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                           </p></td></tr>
<tr>
<td>
<p>timestamp_created   </p></td>
<td>
<p>datetime      </p></td>
<td>
<p>                           </p></td></tr>
<tr>
<td>
<p>timestamp_updated   </p></td>
<td>
<p>datetime      </p></td>
<td>
<p>                           </p></td></tr>
<tr>
<td>
<p>license_agreement   </p></td>
<td>
<p>string        </p></td>
<td>
<p>max_length=2048, default=&quot;This advisory has been prepared and is the property of Orange Cyberdefense. Please don't redistribute this content without our agreement.&quot; </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Content Blocks</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="f28c7052-5040-48f2-9166-255a977dd393">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id                 </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>advisory           </p></td>
<td>
<p>integer       </p></td>
<td>
<p>not null                 </p></td></tr>
<tr>
<td>
<p>index              </p></td>
<td>
<p>integer       </p></td>
<td>
<p>default=0, null=False, minimum=0</p></td></tr>
<tr>
<td>
<p>title              </p></td>
<td>
<p>string        </p></td>
<td>
<p>max_length=200            </p></td></tr>
<tr>
<td>
<p>severity           </p></td>
<td>
<p>integer       </p></td>
<td>
<p>allowed_range [0, 5]                   </p></td></tr>
<tr>
<td>
<p>analyst            </p></td>
<td>
<p>integer       </p></td>
<td>
<p>null=True                </p></td></tr>
<tr>
<td>
<p>last_modified_by   </p></td>
<td>
<p>integer       </p></td>
<td>
<p>null=True                </p></td></tr>
<tr>
<td>
<p>executive_summary  </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>what_you_will_hear </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>what_it_means      </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>what_you_should_do </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>what_we_are_doing  </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>other              </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>threat_category    </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>timestamp_created  </p></td>
<td>
<p>datetime      </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>timestamp_updated  </p></td>
<td>
<p>datetime      </p></td>
<td>
<p>                         </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Sources</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="f9a61e24-9e1d-4c33-a186-3d146b80cda2">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id               </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>content_block    </p></td>
<td>
<p>integer       </p></td>
<td>
<p>not null                 </p></td></tr>
<tr>
<td>
<p>title            </p></td>
<td>
<p>string        </p></td>
<td>
<p>default=&rdquo;&rdquo;</p></td></tr>
<tr>
<td>
<p>description      </p></td>
<td>
<p>text          </p></td>
<td>
<p>blank=true               </p></td></tr>
<tr>
<td>
<p>url              </p></td>
<td>
<p>string        </p></td>
<td>
<p>max_length=500           </p></td></tr>
<tr>
<td>
<p>type             </p></td>
<td>
<p>string        </p></td>
<td>
<p>[external, internal]     </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Detection Rules</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="d9f72566-e985-4329-a3da-ede00001fc54">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id               </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>content_block    </p></td>
<td>
<p>integer       </p></td>
<td>
<p>not null                 </p></td></tr>
<tr>
<td>
<p>title            </p></td>
<td>
<p>string        </p></td>
<td>
<p>default=&rdquo;&rdquo;</p></td></tr>
<tr>
<td>
<p>description      </p></td>
<td>
<p>text          </p></td>
<td>
<p>blank=true               </p></td></tr>
<tr>
<td>
<p>content          </p></td>
<td>
<p>text          </p></td>
<td>
<p>                         </p></td></tr></tbody></table>
<hr />
<h3>Table: <code>Datalake Url</code></h3>
<table data-table-width="760" data-layout="default" ac:local-id="16271f7b-4714-456b-ad7a-e7587c824a01">
<tbody>
<tr>
<th>
<p>Column</p></th>
<th>
<p>Type</p></th>
<th>
<p>Constraints</p></th></tr>
<tr>
<td>
<p>id               </p></td>
<td>
<p>integer       </p></td>
<td>
<p>                         </p></td></tr>
<tr>
<td>
<p>content_block    </p></td>
<td>
<p>integer       </p></td>
<td>
<p>not null                 </p></td></tr>
<tr>
<td>
<p>title            </p></td>
<td>
<p>string        </p></td>
<td>
<p>default=&rdquo;&rdquo;    </p></td></tr>
<tr>
<td>
<p>description      </p></td>
<td>
<p>text          </p></td>
<td>
<p>blank=true               </p></td></tr>
<tr>
<td>
<p>url              </p></td>
<td>
<p>string        </p></td>
<td>
<p>max_length=500           </p></td></tr></tbody></table>
<h1>API</h1>
<h2>Request fields validation</h2>
<p>Errors related to parsing requests fields, are returned in format: </p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="a600913a-418d-4413-8541-de256f4e294a"><ac:plain-text-body><![CDATA[{
  "detail": [
    {
      "loc": [],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}]]></ac:plain-text-body></ac:structured-macro>
<p><code>loc</code> - shows the field when the error occured</p>
<p><code>msg</code> - is the error message</p>
<p><code>type</code> - is type of error</p>
<p />
<p>For example:</p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="f5baef0f-21ff-49a2-b687-2f61913ff60c"><ac:parameter ac:name="language">json</ac:parameter><ac:plain-text-body><![CDATA[{
  "detail": [
    {
      "loc": [
        "body",
        "user_data",
        "email"
      ],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    },
    {
      "loc": [
        "body",
        "user_data",
        "first_name"
      ],
      "msg": "str type expected",
      "type": "type_error.str"
    },
    {
      "loc": [
        "body",
        "user_data",
        "last_name"
      ],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {
        "limit_value": 1
      }
    }
  ]
}]]></ac:plain-text-body></ac:structured-macro>
<h2>Errors</h2>
<p>Errors that occurs when processing requests, creating models, authentication, checking permissions are returned in format: <code>{&quot;detail&quot;: &quot;error message&quot;}</code></p>
<h2>Dates</h2>
<p>Date passed in requests will be treated as UTC except the cases when the timezone is passed in timestamp string.</p>
<h2>Permissions</h2>
<p>If not met, returns error <code>You do not have permissions to perform this action.</code> with status code <code>403</code></p>
<h2>Pagination</h2>
<p><code>Limit</code> and <code>Offset</code> can be set as query params for listing <code>users</code>, <code>content_block</code>, <code>advisories</code>, <code>threat_categories</code>, <code>sources</code>, <code>detection_rules</code>, <code>tags</code>, and <code>datalake_url</code>. Default limit is set in ENV <code>PAGINATION_PER_PAGE</code>.</p>
<h1>Endpoints</h1>
<h2>Auth</h2>
<h3>Login</h3>
<p><strong>URL: </strong><code>/api/auth/login</code></p>
<p><strong>Permissions: </strong><code>Not set</code></p>
<p><strong>Authorization: </strong><code>Not set</code></p>
<p><strong>Throttling: </strong><code>ANON_REQUESTS_PER_MIN</code> /</p>
<p><strong>Description: </strong></p>
<p>Endpoint used to authenticate users email and password. In response user receive a key that is used to access other endpoints related to users and API keys.</p>
<p>User can be authenticated only if it exists in database and <code>is_active</code> flag is set to <code>True</code>.</p>
<p>After authentication user receive a <code>LoginToken</code> if it exists. If the token doesn&rsquo;t exist, a new one is created with 8 hours expiration. If the token expires, it will be refreshed when user log in again.</p>
<p>If authentication fails, an error <code>Authentication failed, please verify if your account is active</code> will be returned with status code <code>401</code>.</p>
<h2>Users</h2>
<h3><strong>Get Users</strong></h3>
<p><strong>URL: </strong><code>/api/users</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get list of users. It returns only the users that are descendants of the requesting user.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/users</code> (<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new user with <code>manager</code> field set to the creating user. </p>
<p>When user is created by <code>MANAGER</code>, the values of <code>active_until</code>, <code>company</code> and <code>department</code> are set to values of the creating manager. Otherwise value of <code>active_until</code> is set to default value (365 days).</p>
<p>The email is validated by <code>EmailStr</code> type of <a href="https://docs.pydantic.dev/1.10/usage/types/">pydantic</a> that where it use <a href="https://pypi.org/project/email-validator/">python-email-validator</a> to validate value of email. The email must be unique, if any user with the same email already exists the error will be returned <code>User with email &lt;email&gt; already exists.</code></p>
<p>User is created with default role <code>USER</code>. The other role can be passed in request, but <code>ADMIN</code> user can only be created by other Admin, if the creator role is different than <code>ADMIN</code> the error will be raised: <code>User with role: admin can be created by user with role admin.</code></p>
<p>If creating <code>ADMIN</code> when the number of active admins is max returns error <code>Maximum number of admins has been reached.</code></p>
<h3><strong>Get Own Data</strong></h3>
<p><strong>URL: </strong><code>/api/users/self</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get data of requesting user.</p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get data of user for given id. </p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Edit One</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}</code> (<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update data of user for given id. </p>
<p>Fields that can be updated: <code>first_name</code>, <code>last_name</code>, <code>phone_number</code>, <code>manager</code>, <code>department</code>, <code>country</code>, <code>active_until</code>. All are optional.</p>
<p>Phone number should be passed in international format (starting with <code>+</code>).</p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is self or it&rsquo;s not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<p>If requesting user is not <code>MANAGER</code> or <code>ADMIN</code> and tries to change <code>manager</code> field it returns error <code>User with role {role} cannot set manager.</code> with status code <code>403</code>.</p>
<p>If changing <code>manager</code> field but the manager is not found returns error <code>User not found for id: {manager_id}.</code> with status code <code>404</code>. If the manager is not descendant of requesting user returns <code>You do not have permission to access user: {manager_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Edit Role</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/role</code> (<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update role of user for given id. </p>
<p>If changing role from <code>ADMIN</code> or <code>MANAGER</code> to a new one that is not one of them all of descendants of changed user will have <code>manager</code> field set to the requesting user.</p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<p>If changing role to <code>ANALYST</code> or <code>ADMIN</code> but requesting user is not admin returns error <code>User with role: {requesting_user_role} cannot change users role to {new_role}.</code> with status code <code>403</code>.</p>
<p>If changing role to <code>ADMIN</code> when the number of active admins is max returns error <code>Maximum number of admins has been reached.</code></p>
<h3><strong>Edit Company</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/company</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update company of user for given id and all of his descendants. </p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Edit Descendants</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/set_descendants</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to set manager of users for given ids.</p>
<p>Returns list of users ids with result messages in format <code>{id: message}</code>:</p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="e67698f5-6e86-437e-913e-ad5113bb20da"><ac:parameter ac:name="language">py</ac:parameter><ac:plain-text-body><![CDATA[{
  "assignments": {
      {descendant_id}: "Success",
      {not_existing_id}: "User not found for id: {not_existing_id}.",
      {not_descendant_id}: "You do not have permission to access user: {not_descendant_id}."
  }
}]]></ac:plain-text-body></ac:structured-macro>
<p>If any user is not found message error is <code>User not found for id: {user_id}.</code>.</p>
<p>If any user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code>.</p>
<h3><strong>Edit Activation</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/set_activation</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to set <code>is_active</code> field to requested value of user for given id. </p>
<p>If the <code>is_active</code> is being set to <code>False</code> it also revokes all keys of that user. If the <code>is_active</code> is being set to <code>True</code> is also updates <code>active_until</code> field to same value of requesting user or to default value if the requested user is Admin. </p>
<p>If the <code>with_descendants</code> flag is <code>True</code> it also do the same changes for all of descendants. If the <code>with_descendants</code> flag is <code>False</code> <code>manager</code> of descendants is set to requesting user.</p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}</code> (<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ADMIN</code>, <code>MANAGER</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete user for given id. Returns <code>204</code> status code if no errors occurs.</p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Send Invitation</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/send_invitation</code> (<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ADMIN</code>, <code>MANAGER</code></p>
<p><strong>Authorization: </strong><code>LoginTokenAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to send invitation email to user for given id.</p>
<p>It creates <code>EmailKey</code> with 8h expiration and send it in the email body.</p>
<p>In the email user receive link to API Docs, where user can activate the account.</p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="943dced9-46f9-406a-b266-7d5b1b8216b3"><ac:plain-text-body><![CDATA[To activate Account authenticate in docs: {{ docs_url }} using "EmailKeyAuthentication"
then use "Activate" endpoint.

Your authentication key is:
"EmailKeyAuthentication": "{{token_key}}".
]]></ac:plain-text-body></ac:structured-macro>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<p>If the user is already verified returns error <code>User has been already verified</code> with status code <code>400</code>.</p>
<h3><strong>Activate Account</strong></h3>
<p><strong>URL: </strong><code>/api/users/activate</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>EmailKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to verify user for given <code>EmailKey</code>. It set <code>verified</code> flag to <code>True</code> and set password to given value.</p>
<h3><strong>Request Password Reset</strong></h3>
<p><strong>URL: </strong><code>/api/users/{user_id}/send_password_reset-request</code> (<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>Not set</code></p>
<p><strong>Authorization: </strong><code>Not set</code></p>
<p><strong>Throttling: </strong><code>ANON_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to send invitation email to user for given id. Returns <code>204</code> status code if no error occurs.</p>
<p>It creates <code>EmailKey</code> with 8h expiration and send it in the email body.</p>
<p>In the email user receive link to API Docs, where user can set new password.</p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="8102dd37-913d-412c-b26c-88abf13b8a2b"><ac:plain-text-body><![CDATA[To reset the password authenticate in docs: {{ docs_url }} using "EmailKeyAuthentication"
then use "Reset Password" endpoint.

Your authentication key is:
"EmailKeyAuthentication": "{{token_key}}".

Required data:
{
    "password": "<your new password>"
    "password_confirmation": "<your new password>"
}
]]></ac:plain-text-body></ac:structured-macro>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<h3><strong>Reset Password</strong></h3>
<p><strong>URL: </strong><code>/api/users/reset_password</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>EmailKeyAuthentication</code> or <code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to set password to given value. This will revoke all <code>EmailKeyAuthentication</code> and <code>LoginKeyAuthentication</code>.</p>
<h2>API Keys</h2>
<h3><strong>Get Own Keys</strong></h3>
<p><strong>URL: </strong><code>/api/api_keys/</code>(<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get all API keys of requesting user.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/api_keys/</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create a new API key.</p>
<p>Expiration field is optional. If it&rsquo;s nor passed the expiration date of that key on default is set to 1 year, if the user has lower expiration date it will be set to that value.</p>
<p>If number of existing tokens is already maxed it returns error <code>The limit of the keys is {api_key_max_number}.</code>.</p>
<p>If the value of passed expiration is lower than user expiration it returns error <code>Cannot set expiration date greater than user expiration.</code>.</p>
<h3><strong>Get User Keys</strong></h3>
<p><strong>URL: </strong><code>/api/api_keys/user/{user_id}</code>(<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get all API keys of user for given id.</p>
<p>If the user is not found returns error <code>User not found for id: {user_id}.</code> with status code <code>404</code>.</p>
<p>If the user is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<h3><strong>Update Expiration Date</strong></h3>
<p><strong>URL: </strong><code>/api/api_keys/{token_id}</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update expiration date of key for given id.</p>
<p>If token is not found returns error <code>Not Found</code> with status code <code>404</code>. </p>
<p>If the token owner is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<p>If the value of passed expiration is lower than user expiration it returns error <code>Cannot set expiration date greater than user expiration.</code>.</p>
<h3><strong>Revoke Key</strong></h3>
<p><strong>URL: </strong><code>/api/api_keys/{token_id}/revoke</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>LoginKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to revoke key for given id.</p>
<p>If token is not found returns error <code>Not Found</code> with status code <code>404</code>.</p>
<p>If the token owner is not descendant of requesting user returns <code>You do not have permission to access user: {user_id}.</code> with status code <code>403</code>.</p>
<p />
<h2>Advisory</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/advisory</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of advisories. </p>
<p>List can be filtered by <code>title</code>, <code>content</code>, <code>severity</code>, <code>tags_name</code>, <code>threat_category_title</code>, <code>created_before</code>, <code>created_after</code>, <code>updated_before</code>, <code>updated_after</code>. Filters can be added to request as query params.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/advisory</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new advisory for given data. </p>
<p>If given <code>threat_category</code> is not found the error will be raised: <code>ThreatCategory with title: {title} not found</code> with status code <code>404</code></p>
<p>The <code>tags</code> will be set using existing records, if the records don't exists, new will be created.</p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/advisory/{advisory_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get advisory data for given id.</p>
<p>If <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Edit One</strong></h3>
<p><strong>URL: </strong><code>/api/advisory/{advisory_id}</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update advisory for given data. </p>
<p>If <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code>.</p>
<p>If given <code>threat_category</code> is not found the error will be raised: <code>ThreatCategory with title: {title} not found</code> with status code <code>404</code></p>
<p>The <code>tags</code> will be set using existing records, if the records don't exists, new will be created.</p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/advisory/{advisory_id}</code> (<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete advisory for given data. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code>.</p>
<h3>Get HTML</h3>
<p><strong>URL: </strong><code>/api/advisory/{advisory_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get an advisory as HTML. </p>
<p>If <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code>.</p>
<h3>Get HTML Minimized</h3>
<p><strong>URL: </strong><code>/api/advisory/{advisory_id}/minimized</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to get an advisory as HTML. If there are mote then 6 updates, the HTML will display the latest 5 updates and the initial advisory. </p>
<p>If <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code>.</p>
<h2>Content Block</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/content_block</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of content blocks. </p>
<p>List can be filtered by <code>title</code>, <code>advisory_id</code>, <code>threat_category_title</code>, <code>severity</code>, <code>content</code>, <code>created_before</code>, <code>created_after</code>, <code>updated_before</code>, <code>updated_after</code>,<code>tags_name</code>, <code>sources</code>, <code>detection_rules</code>, <code>datalake_url</code>. Filters can be add to request as query params.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/content_block</code> (<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new content block for given data. </p>
<p>The <code>analyst</code> and <code>last_modified_by</code> are set to user that creates content_block.</p>
<p>If given <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code></p>
<p>If given <code>threat_category</code> is not found the error will be raised: <code>ThreatCategory with title: {title} not found</code> with status code <code>404</code></p>
<p>The <code>tags</code> will be set using existing records, if the records don't exists, new will be created.</p>
<p>If <code>sources</code>, <code>detection_rules</code> or  <code>datalake_url</code> are not found the error will be raised: <code>No {name_of_field} found for given data.</code> with status code <code>404</code></p>
<h3><strong>List All Complete</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/complete</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of content blocks. The endpoint returns additional data <code>executive_summary</code>, <code>what_you_will_hear</code>, <code>what_it_means</code>, <code>what_you_should_do</code>.</p>
<p>List can be filtered by <code>title</code>, <code>advisory_id</code>, <code>threat_category_title</code>, <code>severity</code>, <code>content</code>, <code>created_before</code>, <code>created_after</code>, <code>updated_before</code>, <code>updated_after</code>,<code>tags_name</code>, <code>sources</code>, <code>detection_rules</code>, <code>datalake_url</code>. Filters can be add to request as query params.</p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/{content_block_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get a content block data for given id.</p>
<p>If the content block is not found returns error <code>Content block with id: {content_block_id} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Edit One</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/{content_block_id}</code> (<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update a content block for given data. </p>
<p>If the content_block is not found returns error <code>Content block with id: {content_block_id} not found.</code> with status code <code>404</code>.</p>
<p>The <code>last_modified_by</code> is set to user that updates content block.</p>
<p>If given <code>advisory</code> is not found the error will be raised: <code>Advisory with id: {advisory_id} not found.</code> with status code <code>404</code></p>
<p>If given <code>threat_category</code> is not found the error will be raised: <code>ThreatCategory with title: {title} not found</code> with status code <code>404</code></p>
<p>The <code>tags</code> will be set using existing records, if the records don't exists, new will be created.</p>
<p>If <code>sources</code>, <code>detection_rules</code> or <code>datalake_url</code> are not found the error will be raised: <code>No {name_of_field} found for given data.</code> with status code <code>404</code></p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/{content_block_id}</code> (<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete a content block for given id. Returns <code>204</code> status code if no errors occurs.</p>
<p>If the content_block is not found returns error <code>Content block with id: {content_block_id} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Get One Minimized</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/{content_block_id}/minimized</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get a content block data for given id. The endpoint does not return the content, only the metadata of the block.</p>
<p>If the content block is not found returns error <code>Content block with id: {content_block_id} not found.</code> with status code <code>404</code>.</p>
<p />
<h3><strong>Get HTML</strong></h3>
<p><strong>URL: </strong><code>/api/content_block/{content_block_id}/html</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get a content block as HTML. </p>
<p>If <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found.</code> with status code <code>404</code>.</p>
<p />
<h2>Detection Rule</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/detection_rule</code>(<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of detection rules.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/detection_rule</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new detection rule for given data. </p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code>. </p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/detection_rule/{detection_rule_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get detection_rule data for given id.</p>
<p>If <code>detection_rule</code> is not found the error will be raised: <code>DetectionRule with id: {detection_rule_id} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Edit One</strong></h3>
<p><strong>URL: </strong><code>/api/detection_rule/{detection_rule_id}</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update detection_rule for given data. </p>
<p>If <code>detection_rule</code> is not found the error will be raised: <code>DetectionRule with id: {source_id} not found.</code> with status code <code>404</code>.</p>
<p>If given content_block is <code>None</code> the current content_block will be unlinked.</p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code></p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/detection_rule/{detection_rule_id}</code>(<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete a detection rule for given <code>id</code>. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>detection_rule</code> is not found the error will be raised: <code>DetectionRule with id: {source_id} not found.</code> with status code <code>404</code>.</p>
<h2>Source</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/source</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of sources.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/source</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new source for given data. </p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code></p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/source/{source_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get source data for given id.</p>
<p>If <code>source</code>not found the error will be raised: <code>Source with id {source_id} not found.</code> with status code <code>404</code>.</p>
<h3>Edit One</h3>
<p><strong>URL: </strong><code>/api/source/{source_id}</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update source for given data. </p>
<p>If <code>source</code> is not found the error will be raised: <code>Source with id {source_id} not found.</code> with status code <code>404</code>.</p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code></p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/source/{source_id}</code>(<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete a source for given <code>id</code>. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>source</code> is not found the error will be raised: <code>Source with id {source_id} not found.</code> with status code <code>404</code>.</p>
<h2>Datalake Url</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/datalake_url</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of datalake urls.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/datalake_url</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new datalake url for given data. </p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code></p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/source/{datalake_url_id}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get datalake url data for given id.</p>
<p>If <code>datalake_url</code> not found the error will be raised: <code>DatalakeUrl with id: {datalake_url_id} not found.</code> with status code <code>404</code>.</p>
<h3>Edit One</h3>
<p><strong>URL: </strong><code>/api/source/{datalake_url_id}</code>(<code>PATCH</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to update a datalake url for given data. </p>
<p>If <code>datalake_url</code> is not found the error will be raised: <code>DatalakeUrl with id: {datalake_url_id} not found.</code> with status code <code>404</code>.</p>
<p>If given <code>content_block</code> is not found the error will be raised: <code>Content block with id: {content_block_id} not found</code> with status code <code>404</code></p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/source/{datalake_url_id}</code>(<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete a datalake url for given id. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>datalake_url</code> is not found the error will be raised: <code>DatalakeUrl with id: {datalake_url_id} not found.</code> with status code <code>404</code>.</p>
<h2>Tags</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/tags</code>(<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of tags.</p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/tags</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new tag for given data. </p>
<p>Tag name is unique. When creating tag with existing name the error will be raised: <code>Tag with name {name} already eixsts.</code></p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/tags/{tag_name}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get tag data for given name.</p>
<p>If <code>tag</code> is not found the error will be raised: <code>Tag with name {tag_name} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/tags/{tag_name}</code>(<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete tag for given data. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>tag</code> is not found the error will be raised: <code>Tag with name {tag_name} not found.</code> with status code <code>404</code>.</p>
<p />
<h2>Threat Category</h2>
<h3><strong>List All</strong></h3>
<p><strong>URL: </strong><code>/api/threat_category</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get list of threat categories. </p>
<h3><strong>Create One</strong></h3>
<p><strong>URL: </strong><code>/api/threat_category</code>(<code>POST</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to create new threat category for given data. </p>
<p>Threat category title is unique. When trying to create a record with existing title the error will be raised: <code>ThreatCategory with title {title} already exists.</code> with status code <code>400</code></p>
<h3><strong>Get One</strong></h3>
<p><strong>URL: </strong><code>/api/threat_category /{threat_category_title}</code> (<code>GET</code>)</p>
<p><strong>Permissions: </strong><code>MANAGER</code>, <code>ADMIN</code>, <code>ANALYST</code>, <code>USER</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code></p>
<p><strong>Description:</strong></p>
<p>Endpoint used to get threat category data for given title.</p>
<p>If <code>threat_category</code>is not found the error will be raised: <code>ThreatCategory with title: {threat_category_title} not found.</code> with status code <code>404</code>.</p>
<h3><strong>Delete One</strong></h3>
<p><strong>URL: </strong><code>/api/threat_category/{threat_category_title}</code>(<code>DELETE</code>)</p>
<p><strong>Permissions: </strong><code>ANALYST</code>, <code>ADMIN</code></p>
<p><strong>Authorization: </strong><code>APIKeyAuthentication</code></p>
<p><strong>Throttling: </strong><code>USER_REQUESTS_PER_MIN</code> </p>
<p><strong>Description: </strong></p>
<p>Endpoint used to delete a threat category for given title. Returns <code>204</code> status code if no errors occurs.</p>
<p>If <code>threat_category</code>is not found the error will be raised: <code>ThreatCategory with title: {threat_category_title} not found.</code> with status code <code>404</code>.</p>
<p />


 
