'''
# CDKTF Metaflow on AWS
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Metaflow(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.Metaflow",
):
    '''Defines an Metaflow based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4 outerbounds/metaflow/aws}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enable_step_functions: builtins.bool,
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        vpc_cidr_blocks: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        with_public_ip: builtins.bool,
        access_list_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_type: typing.Optional[builtins.str] = None,
        compute_environment_desired_vcpus: typing.Optional[jsii.Number] = None,
        compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_max_vcpus: typing.Optional[jsii.Number] = None,
        compute_environment_min_vcpus: typing.Optional[jsii.Number] = None,
        enable_custom_batch_container_registry: typing.Optional[builtins.bool] = None,
        extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        launch_template_http_endpoint: typing.Optional[builtins.str] = None,
        launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        launch_template_http_tokens: typing.Optional[builtins.str] = None,
        metadata_service_container_image: typing.Optional[builtins.str] = None,
        metadata_service_enable_api_basic_auth: typing.Optional[builtins.bool] = None,
        metadata_service_enable_api_gateway: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Any = None,
        resource_suffix: typing.Any = None,
        ui_alb_internal: typing.Optional[builtins.bool] = None,
        ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_certificate_arn: typing.Optional[builtins.str] = None,
        ui_static_container_image: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param enable_step_functions: Provisions infrastructure for step functions if enabled.
        :param subnet1_id: First subnet used for availability zone redundancy.
        :param subnet2_id: Second subnet used for availability zone redundancy.
        :param tags: aws tags The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}.
        :param vpc_cidr_blocks: The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.
        :param vpc_id: The id of the single VPC we stood up for all Metaflow resources to exist in.
        :param with_public_ip: Enable public IP assignment for the Metadata Service. Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        :param access_list_cidr_blocks: List of CIDRs we want to grant access to our Metaflow Metadata Service. Usually this is our VPN's CIDR blocks.
        :param batch_type: AWS Batch Compute Type ('ec2', 'fargate'). Default: ec2
        :param compute_environment_desired_vcpus: Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate). Default: 8
        :param compute_environment_egress_cidr_blocks: CIDR blocks to which egress is allowed from the Batch Compute environment's security group. Default: 0.0.0.0/0
        :param compute_environment_instance_types: The instance types for the compute environment. Default: c4.large,c4.xlarge,c4.2xlarge,c4.4xlarge,c4.8xlarge
        :param compute_environment_max_vcpus: Maximum VCPUs for Batch Compute Environment [16-96]. Default: 64
        :param compute_environment_min_vcpus: Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate). Default: 8
        :param enable_custom_batch_container_registry: Provisions infrastructure for custom Amazon ECR container registry if enabled.
        :param extra_ui_backend_env_vars: Additional environment variables for UI backend container. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param extra_ui_static_env_vars: Additional environment variables for UI static app. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param force_destroy_s3_bucket: Empty S3 bucket before destroying via terraform destroy.
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param launch_template_http_endpoint: Whether the metadata service is available. Can be 'enabled' or 'disabled' Default: enabled
        :param launch_template_http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. Can be an integer from 1 to 64 Default: 2
        :param launch_template_http_tokens: Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2). Can be 'optional' or 'required' Default: optional
        :param metadata_service_container_image: Container image for metadata service.
        :param metadata_service_enable_api_basic_auth: Enable basic auth for API Gateway? (requires key export) Default: true
        :param metadata_service_enable_api_gateway: Enable API Gateway for public metadata service endpoint. Default: true
        :param resource_prefix: string prefix for all resources. Default: metaflow
        :param resource_suffix: string suffix for all resources.
        :param ui_alb_internal: Defines whether the ALB for the UI is internal.
        :param ui_allow_list: List of CIDRs we want to grant access to our Metaflow UI Service. Usually this is our VPN's CIDR blocks.
        :param ui_certificate_arn: SSL certificate for UI. If set to empty string, UI is disabled.
        :param ui_static_container_image: Container image for the UI frontend app.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c06ad4407f13baa7e439389be7009cb53f5917bf8bb8301d53e60841d5a2f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowConfig(
            enable_step_functions=enable_step_functions,
            subnet1_id=subnet1_id,
            subnet2_id=subnet2_id,
            tags=tags,
            vpc_cidr_blocks=vpc_cidr_blocks,
            vpc_id=vpc_id,
            with_public_ip=with_public_ip,
            access_list_cidr_blocks=access_list_cidr_blocks,
            batch_type=batch_type,
            compute_environment_desired_vcpus=compute_environment_desired_vcpus,
            compute_environment_egress_cidr_blocks=compute_environment_egress_cidr_blocks,
            compute_environment_instance_types=compute_environment_instance_types,
            compute_environment_max_vcpus=compute_environment_max_vcpus,
            compute_environment_min_vcpus=compute_environment_min_vcpus,
            enable_custom_batch_container_registry=enable_custom_batch_container_registry,
            extra_ui_backend_env_vars=extra_ui_backend_env_vars,
            extra_ui_static_env_vars=extra_ui_static_env_vars,
            force_destroy_s3_bucket=force_destroy_s3_bucket,
            iam_partition=iam_partition,
            launch_template_http_endpoint=launch_template_http_endpoint,
            launch_template_http_put_response_hop_limit=launch_template_http_put_response_hop_limit,
            launch_template_http_tokens=launch_template_http_tokens,
            metadata_service_container_image=metadata_service_container_image,
            metadata_service_enable_api_basic_auth=metadata_service_enable_api_basic_auth,
            metadata_service_enable_api_gateway=metadata_service_enable_api_gateway,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            ui_alb_internal=ui_alb_internal,
            ui_allow_list=ui_allow_list,
            ui_certificate_arn=ui_certificate_arn,
            ui_static_container_image=ui_static_container_image,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRestApiIdKeyIdOutput")
    def api_gateway_rest_api_id_key_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGatewayRestApiIdKeyIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="batchComputeEnvironmentSecurityGroupIdOutput")
    def batch_compute_environment_security_group_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchComputeEnvironmentSecurityGroupIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreS3BucketKmsKeyArnOutput")
    def datastore_s3_bucket_kms_key_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastoreS3BucketKmsKeyArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metadataSvcEcsTaskRoleArnOutput")
    def metadata_svc_ecs_task_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataSvcEcsTaskRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowApiGatewayRestApiIdOutput")
    def metaflow_api_gateway_rest_api_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowApiGatewayRestApiIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowBatchContainerImageOutput")
    def metaflow_batch_container_image_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowBatchContainerImageOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowBatchJobQueueOutput")
    def metaflow_batch_job_queue_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowBatchJobQueueOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowDatastoreSysrootS3Output")
    def metaflow_datastore_sysroot_s3_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowDatastoreSysrootS3Output"))

    @builtins.property
    @jsii.member(jsii_name="metaflowDatatoolsS3RootOutput")
    def metaflow_datatools_s3_root_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowDatatoolsS3RootOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowEcsS3AccessIamRoleOutput")
    def metaflow_ecs_s3_access_iam_role_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowEcsS3AccessIamRoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowEventsSfnAccessIamRoleOutput")
    def metaflow_events_sfn_access_iam_role_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowEventsSfnAccessIamRoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowProfileJsonOutput")
    def metaflow_profile_json_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowProfileJsonOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowS3BucketArnOutput")
    def metaflow_s3_bucket_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowS3BucketArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowS3BucketNameOutput")
    def metaflow_s3_bucket_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowS3BucketNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowServiceInternalUrlOutput")
    def metaflow_service_internal_url_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowServiceInternalUrlOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowServiceUrlOutput")
    def metaflow_service_url_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowServiceUrlOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowSfnDynamoDbTableOutput")
    def metaflow_sfn_dynamo_db_table_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowSfnDynamoDbTableOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowSfnIamRoleOutput")
    def metaflow_sfn_iam_role_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowSfnIamRoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="migrationFunctionArnOutput")
    def migration_function_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "migrationFunctionArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="uiAlbArnOutput")
    def ui_alb_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uiAlbArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="uiAlbDnsNameOutput")
    def ui_alb_dns_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uiAlbDnsNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="enableStepFunctions")
    def enable_step_functions(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "enableStepFunctions"))

    @enable_step_functions.setter
    def enable_step_functions(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb50281ad55eb00ca03f6762a1443bbe78e5bd31c4d27900d6e0ae9f9bf7fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStepFunctions", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff6d39379d3599872dc31929f887c1be67862648326f34149282ad1aca244d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3104ef85cbfa0eecdce98973443469d7624e1f6aa06060ebad38456d2dabef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="subnet1Id")
    def subnet1_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet1Id"))

    @subnet1_id.setter
    def subnet1_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c532d1cc3c745c3b2ccec31aead3b3e91fdf75cb56295823cf9906777e726152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet1Id", value)

    @builtins.property
    @jsii.member(jsii_name="subnet2Id")
    def subnet2_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet2Id"))

    @subnet2_id.setter
    def subnet2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea21d93f5e88f978a16a43144209f48445922f020105aacd3abe5cc6cadf1b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet2Id", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478e049146dcb4ee8a5f4531a5a7f14d0758cee6344aa2052083d1c08d4ad097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vpcCidrBlocks")
    def vpc_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcCidrBlocks"))

    @vpc_cidr_blocks.setter
    def vpc_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c9778cb6c92698b4f839d39ebbca09d0a8f022826361ae20e3b83a6ef64265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49d45ffe17715cb7ae4531b41849c25fa850f0b5b431fd2d6bb6e661669fd78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="withPublicIp")
    def with_public_ip(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "withPublicIp"))

    @with_public_ip.setter
    def with_public_ip(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee4c67d85d6e5fc036d39d3f361b783407c8a5f8d50618dfae32a5225a03c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="accessListCidrBlocks")
    def access_list_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessListCidrBlocks"))

    @access_list_cidr_blocks.setter
    def access_list_cidr_blocks(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1973e042217de6e6f5b280091fdf9b3dcbd2de2cabc7bafb7361b01ed197ed46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessListCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="batchType")
    def batch_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "batchType"))

    @batch_type.setter
    def batch_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676a229b069adc690f1052b9d6f132c397e0e62954f1a452c261b6302a582105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchType", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentDesiredVcpus")
    def compute_environment_desired_vcpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeEnvironmentDesiredVcpus"))

    @compute_environment_desired_vcpus.setter
    def compute_environment_desired_vcpus(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf24682646d2876fcf96698ebcea5d6d0f10cea43df8ce73deb31c35e45dc3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentDesiredVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentEgressCidrBlocks")
    def compute_environment_egress_cidr_blocks(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "computeEnvironmentEgressCidrBlocks"))

    @compute_environment_egress_cidr_blocks.setter
    def compute_environment_egress_cidr_blocks(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d6e2f71358314e2f37ba23d9b7d4e607e75607c2bfbd0fb6dcc40ed9672e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentEgressCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentInstanceTypes")
    def compute_environment_instance_types(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "computeEnvironmentInstanceTypes"))

    @compute_environment_instance_types.setter
    def compute_environment_instance_types(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d59d5cc8a6a683dcf1987cb086023905a765427846e5ba3390474360d01dafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentInstanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentMaxVcpus")
    def compute_environment_max_vcpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeEnvironmentMaxVcpus"))

    @compute_environment_max_vcpus.setter
    def compute_environment_max_vcpus(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772c2bc41942fda9cc20de5b9b6848c89a651cc8b42b7f5ae478f75fd6fd0892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentMaxVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentMinVcpus")
    def compute_environment_min_vcpus(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeEnvironmentMinVcpus"))

    @compute_environment_min_vcpus.setter
    def compute_environment_min_vcpus(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a414061d9859747dcb427c2a19f6f22a1fe080cabe5cca6eaebdac35a485be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentMinVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="enableCustomBatchContainerRegistry")
    def enable_custom_batch_container_registry(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableCustomBatchContainerRegistry"))

    @enable_custom_batch_container_registry.setter
    def enable_custom_batch_container_registry(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd147f412a8b39ef0f8167b70b73c49681a6edf04a7a32e41fee08cba7b06b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCustomBatchContainerRegistry", value)

    @builtins.property
    @jsii.member(jsii_name="extraUiBackendEnvVars")
    def extra_ui_backend_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraUiBackendEnvVars"))

    @extra_ui_backend_env_vars.setter
    def extra_ui_backend_env_vars(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e756c9d0c1c70d93e99b5d430fefc9d06031fd596e7e0ddec8670e708dcef27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraUiBackendEnvVars", value)

    @builtins.property
    @jsii.member(jsii_name="extraUiStaticEnvVars")
    def extra_ui_static_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraUiStaticEnvVars"))

    @extra_ui_static_env_vars.setter
    def extra_ui_static_env_vars(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a3b53a82e6405da1718e3029d7c188d7406563024ec0f40d3f1042279d203a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraUiStaticEnvVars", value)

    @builtins.property
    @jsii.member(jsii_name="forceDestroyS3Bucket")
    def force_destroy_s3_bucket(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "forceDestroyS3Bucket"))

    @force_destroy_s3_bucket.setter
    def force_destroy_s3_bucket(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d2795d7bc6f9added7e3e24214eaf15d16547f6d985637334d44d5c49e6d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroyS3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="iamPartition")
    def iam_partition(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamPartition"))

    @iam_partition.setter
    def iam_partition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f127554094db4bdc6921aee6184aa9381392bb785787ecb8de3b9fc338936be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPartition", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpEndpoint")
    def launch_template_http_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateHttpEndpoint"))

    @launch_template_http_endpoint.setter
    def launch_template_http_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6c9c5b35ac8306bdba4892798aaf6174403d9ca5bfef9f2b18e5c0ebf0dd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpPutResponseHopLimit")
    def launch_template_http_put_response_hop_limit(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "launchTemplateHttpPutResponseHopLimit"))

    @launch_template_http_put_response_hop_limit.setter
    def launch_template_http_put_response_hop_limit(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f64c48c0a92a0a558b47778f4c4beccb8db9986204bfe31e478d7871060b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpPutResponseHopLimit", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpTokens")
    def launch_template_http_tokens(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateHttpTokens"))

    @launch_template_http_tokens.setter
    def launch_template_http_tokens(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0704370647cc87d9018fee61de4b4849ea6771c17ea86b16bb294a8ac39ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpTokens", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceContainerImage")
    def metadata_service_container_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataServiceContainerImage"))

    @metadata_service_container_image.setter
    def metadata_service_container_image(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4c7bcbb581d4d67565bf77b7a9e59779b23a7516252f8fd4a1e6b95a075273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceContainerImage", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceEnableApiBasicAuth")
    def metadata_service_enable_api_basic_auth(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "metadataServiceEnableApiBasicAuth"))

    @metadata_service_enable_api_basic_auth.setter
    def metadata_service_enable_api_basic_auth(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b822d8fb37c4a8eae79447e95fe73ff9b4ed6f363429e3ac40a44afaec25139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceEnableApiBasicAuth", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceEnableApiGateway")
    def metadata_service_enable_api_gateway(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "metadataServiceEnableApiGateway"))

    @metadata_service_enable_api_gateway.setter
    def metadata_service_enable_api_gateway(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e8990133329003472e3bd91c40a28505c11fb7a6c1c52ec1a99f0dc411969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceEnableApiGateway", value)

    @builtins.property
    @jsii.member(jsii_name="uiAlbInternal")
    def ui_alb_internal(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "uiAlbInternal"))

    @ui_alb_internal.setter
    def ui_alb_internal(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6690c3a0558f331145d42546286abb0b85614a3846c1003d89dce0c8ee3038b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiAlbInternal", value)

    @builtins.property
    @jsii.member(jsii_name="uiAllowList")
    def ui_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "uiAllowList"))

    @ui_allow_list.setter
    def ui_allow_list(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7601bed4137cb8da1d8ac6b8140a5de45a85a74b19c6cefd4fc224107a248205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiAllowList", value)

    @builtins.property
    @jsii.member(jsii_name="uiCertificateArn")
    def ui_certificate_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiCertificateArn"))

    @ui_certificate_arn.setter
    def ui_certificate_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55984efcfa102463add4923b3a85fedd463f4cf50db266b4751651a04ebfea92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiCertificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="uiStaticContainerImage")
    def ui_static_container_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiStaticContainerImage"))

    @ui_static_container_image.setter
    def ui_static_container_image(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aad21182d95ab0878c87830af84225091693ac73034c5f263fa98da022653de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiStaticContainerImage", value)


class MetaflowCommon(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowCommon",
):
    '''Defines an MetaflowCommon based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/common outerbounds/metaflow/aws//modules/common}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829841cfa9884aede1cde2a81e6bcce493a0fd5a84870ef5e8bcdc0283c09260)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowCommonConfig(
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="defaultMetadataServiceContainerImageOutput")
    def default_metadata_service_container_image_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultMetadataServiceContainerImageOutput"))

    @builtins.property
    @jsii.member(jsii_name="defaultUiStaticContainerImageOutput")
    def default_ui_static_container_image_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultUiStaticContainerImageOutput"))


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowCommonConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
    },
)
class MetaflowCommonConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edee3089650317e6ec3c36b0314673fc212dd01f36da7c96d6d898dae56b3f1f)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowCommonConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowComputation(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowComputation",
):
    '''Defines an MetaflowComputation based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/computation outerbounds/metaflow/aws//modules/computation}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_environment_desired_vcpus: jsii.Number,
        compute_environment_instance_types: typing.Sequence[builtins.str],
        compute_environment_max_vcpus: jsii.Number,
        compute_environment_min_vcpus: jsii.Number,
        metaflow_vpc_id: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        batch_type: typing.Optional[builtins.str] = None,
        compute_environment_additional_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_allocation_strategy: typing.Optional[builtins.str] = None,
        compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        launch_template_http_endpoint: typing.Optional[builtins.str] = None,
        launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        launch_template_http_tokens: typing.Optional[builtins.str] = None,
        launch_template_image_id: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_environment_desired_vcpus: Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).
        :param compute_environment_instance_types: The instance types for the compute environment as a comma-separated list.
        :param compute_environment_max_vcpus: Maximum VCPUs for Batch Compute Environment [16-96].
        :param compute_environment_min_vcpus: Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: The first private subnet used for redundancy.
        :param subnet2_id: The second private subnet used for redundancy.
        :param batch_type: AWS Batch Compute Type ('ec2', 'fargate'). Default: ec2
        :param compute_environment_additional_security_group_ids: Additional security group ids to apply to the Batch Compute environment.
        :param compute_environment_allocation_strategy: Allocation strategy for Batch Compute environment (BEST_FIT, BEST_FIT_PROGRESSIVE, SPOT_CAPACITY_OPTIMIZED). Default: BEST_FIT
        :param compute_environment_egress_cidr_blocks: CIDR blocks to which egress is allowed from the Batch Compute environment's security group. Default: 0.0.0.0/0
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param launch_template_http_endpoint: Whether the metadata service is available. Can be 'enabled' or 'disabled' Default: enabled
        :param launch_template_http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. Can be an integer from 1 to 64 Default: 2
        :param launch_template_http_tokens: Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2). Can be 'optional' or 'required' Default: optional
        :param launch_template_image_id: AMI id for launch template, defaults to allow AWS Batch to decide.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f983a1998df315902d0c7e7a0fb25570052d3a26ce5698308015b3a7a9130f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowComputationConfig(
            compute_environment_desired_vcpus=compute_environment_desired_vcpus,
            compute_environment_instance_types=compute_environment_instance_types,
            compute_environment_max_vcpus=compute_environment_max_vcpus,
            compute_environment_min_vcpus=compute_environment_min_vcpus,
            metaflow_vpc_id=metaflow_vpc_id,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            standard_tags=standard_tags,
            subnet1_id=subnet1_id,
            subnet2_id=subnet2_id,
            batch_type=batch_type,
            compute_environment_additional_security_group_ids=compute_environment_additional_security_group_ids,
            compute_environment_allocation_strategy=compute_environment_allocation_strategy,
            compute_environment_egress_cidr_blocks=compute_environment_egress_cidr_blocks,
            iam_partition=iam_partition,
            launch_template_http_endpoint=launch_template_http_endpoint,
            launch_template_http_put_response_hop_limit=launch_template_http_put_response_hop_limit,
            launch_template_http_tokens=launch_template_http_tokens,
            launch_template_image_id=launch_template_image_id,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="batchComputeEnvironmentSecurityGroupIdOutput")
    def batch_compute_environment_security_group_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchComputeEnvironmentSecurityGroupIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="batchJobQueueArnOutput")
    def batch_job_queue_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchJobQueueArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="ecsExecutionRoleArnOutput")
    def ecs_execution_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsExecutionRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="ecsInstanceRoleArnOutput")
    def ecs_instance_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsInstanceRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowBatchJobQueueOutput")
    def metaflow_batch_job_queue_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowBatchJobQueueOutput"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentDesiredVcpus")
    def compute_environment_desired_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeEnvironmentDesiredVcpus"))

    @compute_environment_desired_vcpus.setter
    def compute_environment_desired_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57062ffa92f7a58dae40a2f134889f76d10a4d19ad4d86ebe3efb4ae2a8e862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentDesiredVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentInstanceTypes")
    def compute_environment_instance_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "computeEnvironmentInstanceTypes"))

    @compute_environment_instance_types.setter
    def compute_environment_instance_types(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065cf6c52a834ffeb56e26fc492d7d2935035e47b2a22a76efccad70c78d2754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentInstanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentMaxVcpus")
    def compute_environment_max_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeEnvironmentMaxVcpus"))

    @compute_environment_max_vcpus.setter
    def compute_environment_max_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb48b24e6bcdf5a72b558b27c51854727d4a3ec24670e1468b1b136461b44560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentMaxVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentMinVcpus")
    def compute_environment_min_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeEnvironmentMinVcpus"))

    @compute_environment_min_vcpus.setter
    def compute_environment_min_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b14b11ee0d68aa742018b8420ab5add53e1c6183be316c6b55124d8b42324f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentMinVcpus", value)

    @builtins.property
    @jsii.member(jsii_name="metaflowVpcId")
    def metaflow_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowVpcId"))

    @metaflow_vpc_id.setter
    def metaflow_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ca91f38605dea860f051abd00d4e5708502f1fb83478c66fc7138fe053d9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metaflowVpcId", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40ed427e87e9845d794e667a41fd3c52ae37800e624ac5488a244ec78d3e89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4289b858cf5365a8fb0cb6280562bc9f10cab5fd946fc35d018f086e717f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="standardTags")
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "standardTags"))

    @standard_tags.setter
    def standard_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd2126d7b5a6921fef7c8df8f2828d1b2f9a940904716fe61377ab4cff23057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardTags", value)

    @builtins.property
    @jsii.member(jsii_name="subnet1Id")
    def subnet1_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet1Id"))

    @subnet1_id.setter
    def subnet1_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f30d7dc31f769468477fea012169b6ce85386dc14f7fce5bd340f8b4b28374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet1Id", value)

    @builtins.property
    @jsii.member(jsii_name="subnet2Id")
    def subnet2_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet2Id"))

    @subnet2_id.setter
    def subnet2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c09b9e6d383ac82f1d57b61a3f2d88612c28a1c6ab924943d68ca3f25e3842c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet2Id", value)

    @builtins.property
    @jsii.member(jsii_name="batchType")
    def batch_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "batchType"))

    @batch_type.setter
    def batch_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b921e269682b398442728d204bea0c6a9ef787a6e46f73eaae3dbc31d08df3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchType", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentAdditionalSecurityGroupIds")
    def compute_environment_additional_security_group_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "computeEnvironmentAdditionalSecurityGroupIds"))

    @compute_environment_additional_security_group_ids.setter
    def compute_environment_additional_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d70ebcf652e1c3b24eb9176b48f008246eb08aad88a5a4f12a7232e8b6d7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentAdditionalSecurityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentAllocationStrategy")
    def compute_environment_allocation_strategy(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeEnvironmentAllocationStrategy"))

    @compute_environment_allocation_strategy.setter
    def compute_environment_allocation_strategy(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8699cf5f5266ee4d09382d9b5e6d181b5603ec7fb6fd40313c37c3438f219c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentAllocationStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentEgressCidrBlocks")
    def compute_environment_egress_cidr_blocks(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "computeEnvironmentEgressCidrBlocks"))

    @compute_environment_egress_cidr_blocks.setter
    def compute_environment_egress_cidr_blocks(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733bb522b4e82e24a327e4dc7f5d0aed5411073c5c71ceb236c718caa55c76e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentEgressCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="iamPartition")
    def iam_partition(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamPartition"))

    @iam_partition.setter
    def iam_partition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ff2b459476b5cd6ddeacff3f7587bef82e57db83823eb9c0c1d5482e0c8022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPartition", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpEndpoint")
    def launch_template_http_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateHttpEndpoint"))

    @launch_template_http_endpoint.setter
    def launch_template_http_endpoint(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324d8ba07b9a09e4c6d7ef4d778a2e709fe6c5d1e19b351f00ab888a46be65b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpPutResponseHopLimit")
    def launch_template_http_put_response_hop_limit(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "launchTemplateHttpPutResponseHopLimit"))

    @launch_template_http_put_response_hop_limit.setter
    def launch_template_http_put_response_hop_limit(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabefb551e91ad354831b3fc9fdd98337e5eaf41b7492986f8db3bd2818e4592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpPutResponseHopLimit", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateHttpTokens")
    def launch_template_http_tokens(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateHttpTokens"))

    @launch_template_http_tokens.setter
    def launch_template_http_tokens(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bbf4a716fef7912c35298ca15a5e0ddb82769210bd4ebc2ad62ed507d465a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateHttpTokens", value)

    @builtins.property
    @jsii.member(jsii_name="launchTemplateImageId")
    def launch_template_image_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchTemplateImageId"))

    @launch_template_image_id.setter
    def launch_template_image_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc139296daecd54b333e6ba3131e62f86553b1d3806d95babb61f3d2d77caba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchTemplateImageId", value)


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowComputationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "compute_environment_desired_vcpus": "computeEnvironmentDesiredVcpus",
        "compute_environment_instance_types": "computeEnvironmentInstanceTypes",
        "compute_environment_max_vcpus": "computeEnvironmentMaxVcpus",
        "compute_environment_min_vcpus": "computeEnvironmentMinVcpus",
        "metaflow_vpc_id": "metaflowVpcId",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "standard_tags": "standardTags",
        "subnet1_id": "subnet1Id",
        "subnet2_id": "subnet2Id",
        "batch_type": "batchType",
        "compute_environment_additional_security_group_ids": "computeEnvironmentAdditionalSecurityGroupIds",
        "compute_environment_allocation_strategy": "computeEnvironmentAllocationStrategy",
        "compute_environment_egress_cidr_blocks": "computeEnvironmentEgressCidrBlocks",
        "iam_partition": "iamPartition",
        "launch_template_http_endpoint": "launchTemplateHttpEndpoint",
        "launch_template_http_put_response_hop_limit": "launchTemplateHttpPutResponseHopLimit",
        "launch_template_http_tokens": "launchTemplateHttpTokens",
        "launch_template_image_id": "launchTemplateImageId",
    },
)
class MetaflowComputationConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        compute_environment_desired_vcpus: jsii.Number,
        compute_environment_instance_types: typing.Sequence[builtins.str],
        compute_environment_max_vcpus: jsii.Number,
        compute_environment_min_vcpus: jsii.Number,
        metaflow_vpc_id: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        batch_type: typing.Optional[builtins.str] = None,
        compute_environment_additional_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_allocation_strategy: typing.Optional[builtins.str] = None,
        compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        launch_template_http_endpoint: typing.Optional[builtins.str] = None,
        launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        launch_template_http_tokens: typing.Optional[builtins.str] = None,
        launch_template_image_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param compute_environment_desired_vcpus: Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).
        :param compute_environment_instance_types: The instance types for the compute environment as a comma-separated list.
        :param compute_environment_max_vcpus: Maximum VCPUs for Batch Compute Environment [16-96].
        :param compute_environment_min_vcpus: Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: The first private subnet used for redundancy.
        :param subnet2_id: The second private subnet used for redundancy.
        :param batch_type: AWS Batch Compute Type ('ec2', 'fargate'). Default: ec2
        :param compute_environment_additional_security_group_ids: Additional security group ids to apply to the Batch Compute environment.
        :param compute_environment_allocation_strategy: Allocation strategy for Batch Compute environment (BEST_FIT, BEST_FIT_PROGRESSIVE, SPOT_CAPACITY_OPTIMIZED). Default: BEST_FIT
        :param compute_environment_egress_cidr_blocks: CIDR blocks to which egress is allowed from the Batch Compute environment's security group. Default: 0.0.0.0/0
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param launch_template_http_endpoint: Whether the metadata service is available. Can be 'enabled' or 'disabled' Default: enabled
        :param launch_template_http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. Can be an integer from 1 to 64 Default: 2
        :param launch_template_http_tokens: Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2). Can be 'optional' or 'required' Default: optional
        :param launch_template_image_id: AMI id for launch template, defaults to allow AWS Batch to decide.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401da8cd2fddb490d1fa268ca9e57db9a6120e4cc94e907002f2df769fbdba53)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument compute_environment_desired_vcpus", value=compute_environment_desired_vcpus, expected_type=type_hints["compute_environment_desired_vcpus"])
            check_type(argname="argument compute_environment_instance_types", value=compute_environment_instance_types, expected_type=type_hints["compute_environment_instance_types"])
            check_type(argname="argument compute_environment_max_vcpus", value=compute_environment_max_vcpus, expected_type=type_hints["compute_environment_max_vcpus"])
            check_type(argname="argument compute_environment_min_vcpus", value=compute_environment_min_vcpus, expected_type=type_hints["compute_environment_min_vcpus"])
            check_type(argname="argument metaflow_vpc_id", value=metaflow_vpc_id, expected_type=type_hints["metaflow_vpc_id"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument standard_tags", value=standard_tags, expected_type=type_hints["standard_tags"])
            check_type(argname="argument subnet1_id", value=subnet1_id, expected_type=type_hints["subnet1_id"])
            check_type(argname="argument subnet2_id", value=subnet2_id, expected_type=type_hints["subnet2_id"])
            check_type(argname="argument batch_type", value=batch_type, expected_type=type_hints["batch_type"])
            check_type(argname="argument compute_environment_additional_security_group_ids", value=compute_environment_additional_security_group_ids, expected_type=type_hints["compute_environment_additional_security_group_ids"])
            check_type(argname="argument compute_environment_allocation_strategy", value=compute_environment_allocation_strategy, expected_type=type_hints["compute_environment_allocation_strategy"])
            check_type(argname="argument compute_environment_egress_cidr_blocks", value=compute_environment_egress_cidr_blocks, expected_type=type_hints["compute_environment_egress_cidr_blocks"])
            check_type(argname="argument iam_partition", value=iam_partition, expected_type=type_hints["iam_partition"])
            check_type(argname="argument launch_template_http_endpoint", value=launch_template_http_endpoint, expected_type=type_hints["launch_template_http_endpoint"])
            check_type(argname="argument launch_template_http_put_response_hop_limit", value=launch_template_http_put_response_hop_limit, expected_type=type_hints["launch_template_http_put_response_hop_limit"])
            check_type(argname="argument launch_template_http_tokens", value=launch_template_http_tokens, expected_type=type_hints["launch_template_http_tokens"])
            check_type(argname="argument launch_template_image_id", value=launch_template_image_id, expected_type=type_hints["launch_template_image_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_environment_desired_vcpus": compute_environment_desired_vcpus,
            "compute_environment_instance_types": compute_environment_instance_types,
            "compute_environment_max_vcpus": compute_environment_max_vcpus,
            "compute_environment_min_vcpus": compute_environment_min_vcpus,
            "metaflow_vpc_id": metaflow_vpc_id,
            "resource_prefix": resource_prefix,
            "resource_suffix": resource_suffix,
            "standard_tags": standard_tags,
            "subnet1_id": subnet1_id,
            "subnet2_id": subnet2_id,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if batch_type is not None:
            self._values["batch_type"] = batch_type
        if compute_environment_additional_security_group_ids is not None:
            self._values["compute_environment_additional_security_group_ids"] = compute_environment_additional_security_group_ids
        if compute_environment_allocation_strategy is not None:
            self._values["compute_environment_allocation_strategy"] = compute_environment_allocation_strategy
        if compute_environment_egress_cidr_blocks is not None:
            self._values["compute_environment_egress_cidr_blocks"] = compute_environment_egress_cidr_blocks
        if iam_partition is not None:
            self._values["iam_partition"] = iam_partition
        if launch_template_http_endpoint is not None:
            self._values["launch_template_http_endpoint"] = launch_template_http_endpoint
        if launch_template_http_put_response_hop_limit is not None:
            self._values["launch_template_http_put_response_hop_limit"] = launch_template_http_put_response_hop_limit
        if launch_template_http_tokens is not None:
            self._values["launch_template_http_tokens"] = launch_template_http_tokens
        if launch_template_image_id is not None:
            self._values["launch_template_image_id"] = launch_template_image_id

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def compute_environment_desired_vcpus(self) -> jsii.Number:
        '''Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).'''
        result = self._values.get("compute_environment_desired_vcpus")
        assert result is not None, "Required property 'compute_environment_desired_vcpus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def compute_environment_instance_types(self) -> typing.List[builtins.str]:
        '''The instance types for the compute environment as a comma-separated list.'''
        result = self._values.get("compute_environment_instance_types")
        assert result is not None, "Required property 'compute_environment_instance_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def compute_environment_max_vcpus(self) -> jsii.Number:
        '''Maximum VCPUs for Batch Compute Environment [16-96].'''
        result = self._values.get("compute_environment_max_vcpus")
        assert result is not None, "Required property 'compute_environment_max_vcpus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def compute_environment_min_vcpus(self) -> jsii.Number:
        '''Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).'''
        result = self._values.get("compute_environment_min_vcpus")
        assert result is not None, "Required property 'compute_environment_min_vcpus' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metaflow_vpc_id(self) -> builtins.str:
        '''ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.'''
        result = self._values.get("metaflow_vpc_id")
        assert result is not None, "Required property 'metaflow_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_prefix(self) -> builtins.str:
        '''Prefix given to all AWS resources to differentiate between applications.'''
        result = self._values.get("resource_prefix")
        assert result is not None, "Required property 'resource_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_suffix(self) -> builtins.str:
        '''Suffix given to all AWS resources to differentiate between environment and workspace.'''
        result = self._values.get("resource_suffix")
        assert result is not None, "Required property 'resource_suffix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The standard tags to apply to every AWS resource.

        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("standard_tags")
        assert result is not None, "Required property 'standard_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def subnet1_id(self) -> builtins.str:
        '''The first private subnet used for redundancy.'''
        result = self._values.get("subnet1_id")
        assert result is not None, "Required property 'subnet1_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet2_id(self) -> builtins.str:
        '''The second private subnet used for redundancy.'''
        result = self._values.get("subnet2_id")
        assert result is not None, "Required property 'subnet2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_type(self) -> typing.Optional[builtins.str]:
        '''AWS Batch Compute Type ('ec2', 'fargate').

        :default: ec2
        '''
        result = self._values.get("batch_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_environment_additional_security_group_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional security group ids to apply to the Batch Compute environment.'''
        result = self._values.get("compute_environment_additional_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def compute_environment_allocation_strategy(self) -> typing.Optional[builtins.str]:
        '''Allocation strategy for Batch Compute environment (BEST_FIT, BEST_FIT_PROGRESSIVE, SPOT_CAPACITY_OPTIMIZED).

        :default: BEST_FIT
        '''
        result = self._values.get("compute_environment_allocation_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_environment_egress_cidr_blocks(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR blocks to which egress is allowed from the Batch Compute environment's security group.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("compute_environment_egress_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def iam_partition(self) -> typing.Optional[builtins.str]:
        '''IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is).

        :default: aws
        '''
        result = self._values.get("iam_partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_http_endpoint(self) -> typing.Optional[builtins.str]:
        '''Whether the metadata service is available.

        Can be 'enabled' or 'disabled'

        :default: enabled
        '''
        result = self._values.get("launch_template_http_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_http_put_response_hop_limit(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The desired HTTP PUT response hop limit for instance metadata requests.

        Can be an integer from 1 to 64

        :default: 2
        '''
        result = self._values.get("launch_template_http_put_response_hop_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def launch_template_http_tokens(self) -> typing.Optional[builtins.str]:
        '''Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2).

        Can be 'optional' or 'required'

        :default: optional
        '''
        result = self._values.get("launch_template_http_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_image_id(self) -> typing.Optional[builtins.str]:
        '''AMI id for launch template, defaults to allow AWS Batch to decide.'''
        result = self._values.get("launch_template_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowComputationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "enable_step_functions": "enableStepFunctions",
        "subnet1_id": "subnet1Id",
        "subnet2_id": "subnet2Id",
        "tags": "tags",
        "vpc_cidr_blocks": "vpcCidrBlocks",
        "vpc_id": "vpcId",
        "with_public_ip": "withPublicIp",
        "access_list_cidr_blocks": "accessListCidrBlocks",
        "batch_type": "batchType",
        "compute_environment_desired_vcpus": "computeEnvironmentDesiredVcpus",
        "compute_environment_egress_cidr_blocks": "computeEnvironmentEgressCidrBlocks",
        "compute_environment_instance_types": "computeEnvironmentInstanceTypes",
        "compute_environment_max_vcpus": "computeEnvironmentMaxVcpus",
        "compute_environment_min_vcpus": "computeEnvironmentMinVcpus",
        "enable_custom_batch_container_registry": "enableCustomBatchContainerRegistry",
        "extra_ui_backend_env_vars": "extraUiBackendEnvVars",
        "extra_ui_static_env_vars": "extraUiStaticEnvVars",
        "force_destroy_s3_bucket": "forceDestroyS3Bucket",
        "iam_partition": "iamPartition",
        "launch_template_http_endpoint": "launchTemplateHttpEndpoint",
        "launch_template_http_put_response_hop_limit": "launchTemplateHttpPutResponseHopLimit",
        "launch_template_http_tokens": "launchTemplateHttpTokens",
        "metadata_service_container_image": "metadataServiceContainerImage",
        "metadata_service_enable_api_basic_auth": "metadataServiceEnableApiBasicAuth",
        "metadata_service_enable_api_gateway": "metadataServiceEnableApiGateway",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "ui_alb_internal": "uiAlbInternal",
        "ui_allow_list": "uiAllowList",
        "ui_certificate_arn": "uiCertificateArn",
        "ui_static_container_image": "uiStaticContainerImage",
    },
)
class MetaflowConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        enable_step_functions: builtins.bool,
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        vpc_cidr_blocks: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        with_public_ip: builtins.bool,
        access_list_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        batch_type: typing.Optional[builtins.str] = None,
        compute_environment_desired_vcpus: typing.Optional[jsii.Number] = None,
        compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        compute_environment_max_vcpus: typing.Optional[jsii.Number] = None,
        compute_environment_min_vcpus: typing.Optional[jsii.Number] = None,
        enable_custom_batch_container_registry: typing.Optional[builtins.bool] = None,
        extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        launch_template_http_endpoint: typing.Optional[builtins.str] = None,
        launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
        launch_template_http_tokens: typing.Optional[builtins.str] = None,
        metadata_service_container_image: typing.Optional[builtins.str] = None,
        metadata_service_enable_api_basic_auth: typing.Optional[builtins.bool] = None,
        metadata_service_enable_api_gateway: typing.Optional[builtins.bool] = None,
        resource_prefix: typing.Any = None,
        resource_suffix: typing.Any = None,
        ui_alb_internal: typing.Optional[builtins.bool] = None,
        ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_certificate_arn: typing.Optional[builtins.str] = None,
        ui_static_container_image: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param enable_step_functions: Provisions infrastructure for step functions if enabled.
        :param subnet1_id: First subnet used for availability zone redundancy.
        :param subnet2_id: Second subnet used for availability zone redundancy.
        :param tags: aws tags The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}.
        :param vpc_cidr_blocks: The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.
        :param vpc_id: The id of the single VPC we stood up for all Metaflow resources to exist in.
        :param with_public_ip: Enable public IP assignment for the Metadata Service. Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        :param access_list_cidr_blocks: List of CIDRs we want to grant access to our Metaflow Metadata Service. Usually this is our VPN's CIDR blocks.
        :param batch_type: AWS Batch Compute Type ('ec2', 'fargate'). Default: ec2
        :param compute_environment_desired_vcpus: Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate). Default: 8
        :param compute_environment_egress_cidr_blocks: CIDR blocks to which egress is allowed from the Batch Compute environment's security group. Default: 0.0.0.0/0
        :param compute_environment_instance_types: The instance types for the compute environment. Default: c4.large,c4.xlarge,c4.2xlarge,c4.4xlarge,c4.8xlarge
        :param compute_environment_max_vcpus: Maximum VCPUs for Batch Compute Environment [16-96]. Default: 64
        :param compute_environment_min_vcpus: Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate). Default: 8
        :param enable_custom_batch_container_registry: Provisions infrastructure for custom Amazon ECR container registry if enabled.
        :param extra_ui_backend_env_vars: Additional environment variables for UI backend container. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param extra_ui_static_env_vars: Additional environment variables for UI static app. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param force_destroy_s3_bucket: Empty S3 bucket before destroying via terraform destroy.
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param launch_template_http_endpoint: Whether the metadata service is available. Can be 'enabled' or 'disabled' Default: enabled
        :param launch_template_http_put_response_hop_limit: The desired HTTP PUT response hop limit for instance metadata requests. Can be an integer from 1 to 64 Default: 2
        :param launch_template_http_tokens: Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2). Can be 'optional' or 'required' Default: optional
        :param metadata_service_container_image: Container image for metadata service.
        :param metadata_service_enable_api_basic_auth: Enable basic auth for API Gateway? (requires key export) Default: true
        :param metadata_service_enable_api_gateway: Enable API Gateway for public metadata service endpoint. Default: true
        :param resource_prefix: string prefix for all resources. Default: metaflow
        :param resource_suffix: string suffix for all resources.
        :param ui_alb_internal: Defines whether the ALB for the UI is internal.
        :param ui_allow_list: List of CIDRs we want to grant access to our Metaflow UI Service. Usually this is our VPN's CIDR blocks.
        :param ui_certificate_arn: SSL certificate for UI. If set to empty string, UI is disabled.
        :param ui_static_container_image: Container image for the UI frontend app.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b011ea088374cb11d8943508b28b9104cfae57e1e826f167597e09fca21f6cc)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument enable_step_functions", value=enable_step_functions, expected_type=type_hints["enable_step_functions"])
            check_type(argname="argument subnet1_id", value=subnet1_id, expected_type=type_hints["subnet1_id"])
            check_type(argname="argument subnet2_id", value=subnet2_id, expected_type=type_hints["subnet2_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_cidr_blocks", value=vpc_cidr_blocks, expected_type=type_hints["vpc_cidr_blocks"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument with_public_ip", value=with_public_ip, expected_type=type_hints["with_public_ip"])
            check_type(argname="argument access_list_cidr_blocks", value=access_list_cidr_blocks, expected_type=type_hints["access_list_cidr_blocks"])
            check_type(argname="argument batch_type", value=batch_type, expected_type=type_hints["batch_type"])
            check_type(argname="argument compute_environment_desired_vcpus", value=compute_environment_desired_vcpus, expected_type=type_hints["compute_environment_desired_vcpus"])
            check_type(argname="argument compute_environment_egress_cidr_blocks", value=compute_environment_egress_cidr_blocks, expected_type=type_hints["compute_environment_egress_cidr_blocks"])
            check_type(argname="argument compute_environment_instance_types", value=compute_environment_instance_types, expected_type=type_hints["compute_environment_instance_types"])
            check_type(argname="argument compute_environment_max_vcpus", value=compute_environment_max_vcpus, expected_type=type_hints["compute_environment_max_vcpus"])
            check_type(argname="argument compute_environment_min_vcpus", value=compute_environment_min_vcpus, expected_type=type_hints["compute_environment_min_vcpus"])
            check_type(argname="argument enable_custom_batch_container_registry", value=enable_custom_batch_container_registry, expected_type=type_hints["enable_custom_batch_container_registry"])
            check_type(argname="argument extra_ui_backend_env_vars", value=extra_ui_backend_env_vars, expected_type=type_hints["extra_ui_backend_env_vars"])
            check_type(argname="argument extra_ui_static_env_vars", value=extra_ui_static_env_vars, expected_type=type_hints["extra_ui_static_env_vars"])
            check_type(argname="argument force_destroy_s3_bucket", value=force_destroy_s3_bucket, expected_type=type_hints["force_destroy_s3_bucket"])
            check_type(argname="argument iam_partition", value=iam_partition, expected_type=type_hints["iam_partition"])
            check_type(argname="argument launch_template_http_endpoint", value=launch_template_http_endpoint, expected_type=type_hints["launch_template_http_endpoint"])
            check_type(argname="argument launch_template_http_put_response_hop_limit", value=launch_template_http_put_response_hop_limit, expected_type=type_hints["launch_template_http_put_response_hop_limit"])
            check_type(argname="argument launch_template_http_tokens", value=launch_template_http_tokens, expected_type=type_hints["launch_template_http_tokens"])
            check_type(argname="argument metadata_service_container_image", value=metadata_service_container_image, expected_type=type_hints["metadata_service_container_image"])
            check_type(argname="argument metadata_service_enable_api_basic_auth", value=metadata_service_enable_api_basic_auth, expected_type=type_hints["metadata_service_enable_api_basic_auth"])
            check_type(argname="argument metadata_service_enable_api_gateway", value=metadata_service_enable_api_gateway, expected_type=type_hints["metadata_service_enable_api_gateway"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument ui_alb_internal", value=ui_alb_internal, expected_type=type_hints["ui_alb_internal"])
            check_type(argname="argument ui_allow_list", value=ui_allow_list, expected_type=type_hints["ui_allow_list"])
            check_type(argname="argument ui_certificate_arn", value=ui_certificate_arn, expected_type=type_hints["ui_certificate_arn"])
            check_type(argname="argument ui_static_container_image", value=ui_static_container_image, expected_type=type_hints["ui_static_container_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_step_functions": enable_step_functions,
            "subnet1_id": subnet1_id,
            "subnet2_id": subnet2_id,
            "tags": tags,
            "vpc_cidr_blocks": vpc_cidr_blocks,
            "vpc_id": vpc_id,
            "with_public_ip": with_public_ip,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if access_list_cidr_blocks is not None:
            self._values["access_list_cidr_blocks"] = access_list_cidr_blocks
        if batch_type is not None:
            self._values["batch_type"] = batch_type
        if compute_environment_desired_vcpus is not None:
            self._values["compute_environment_desired_vcpus"] = compute_environment_desired_vcpus
        if compute_environment_egress_cidr_blocks is not None:
            self._values["compute_environment_egress_cidr_blocks"] = compute_environment_egress_cidr_blocks
        if compute_environment_instance_types is not None:
            self._values["compute_environment_instance_types"] = compute_environment_instance_types
        if compute_environment_max_vcpus is not None:
            self._values["compute_environment_max_vcpus"] = compute_environment_max_vcpus
        if compute_environment_min_vcpus is not None:
            self._values["compute_environment_min_vcpus"] = compute_environment_min_vcpus
        if enable_custom_batch_container_registry is not None:
            self._values["enable_custom_batch_container_registry"] = enable_custom_batch_container_registry
        if extra_ui_backend_env_vars is not None:
            self._values["extra_ui_backend_env_vars"] = extra_ui_backend_env_vars
        if extra_ui_static_env_vars is not None:
            self._values["extra_ui_static_env_vars"] = extra_ui_static_env_vars
        if force_destroy_s3_bucket is not None:
            self._values["force_destroy_s3_bucket"] = force_destroy_s3_bucket
        if iam_partition is not None:
            self._values["iam_partition"] = iam_partition
        if launch_template_http_endpoint is not None:
            self._values["launch_template_http_endpoint"] = launch_template_http_endpoint
        if launch_template_http_put_response_hop_limit is not None:
            self._values["launch_template_http_put_response_hop_limit"] = launch_template_http_put_response_hop_limit
        if launch_template_http_tokens is not None:
            self._values["launch_template_http_tokens"] = launch_template_http_tokens
        if metadata_service_container_image is not None:
            self._values["metadata_service_container_image"] = metadata_service_container_image
        if metadata_service_enable_api_basic_auth is not None:
            self._values["metadata_service_enable_api_basic_auth"] = metadata_service_enable_api_basic_auth
        if metadata_service_enable_api_gateway is not None:
            self._values["metadata_service_enable_api_gateway"] = metadata_service_enable_api_gateway
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix
        if resource_suffix is not None:
            self._values["resource_suffix"] = resource_suffix
        if ui_alb_internal is not None:
            self._values["ui_alb_internal"] = ui_alb_internal
        if ui_allow_list is not None:
            self._values["ui_allow_list"] = ui_allow_list
        if ui_certificate_arn is not None:
            self._values["ui_certificate_arn"] = ui_certificate_arn
        if ui_static_container_image is not None:
            self._values["ui_static_container_image"] = ui_static_container_image

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_step_functions(self) -> builtins.bool:
        '''Provisions infrastructure for step functions if enabled.'''
        result = self._values.get("enable_step_functions")
        assert result is not None, "Required property 'enable_step_functions' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def subnet1_id(self) -> builtins.str:
        '''First subnet used for availability zone redundancy.'''
        result = self._values.get("subnet1_id")
        assert result is not None, "Required property 'subnet1_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet2_id(self) -> builtins.str:
        '''Second subnet used for availability zone redundancy.'''
        result = self._values.get("subnet2_id")
        assert result is not None, "Required property 'subnet2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''aws tags The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}.'''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def vpc_cidr_blocks(self) -> typing.List[builtins.str]:
        '''The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.'''
        result = self._values.get("vpc_cidr_blocks")
        assert result is not None, "Required property 'vpc_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The id of the single VPC we stood up for all Metaflow resources to exist in.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def with_public_ip(self) -> builtins.bool:
        '''Enable public IP assignment for the Metadata Service.

        Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        '''
        result = self._values.get("with_public_ip")
        assert result is not None, "Required property 'with_public_ip' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def access_list_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CIDRs we want to grant access to our Metaflow Metadata Service.

        Usually this is our VPN's CIDR blocks.
        '''
        result = self._values.get("access_list_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def batch_type(self) -> typing.Optional[builtins.str]:
        '''AWS Batch Compute Type ('ec2', 'fargate').

        :default: ec2
        '''
        result = self._values.get("batch_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_environment_desired_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Desired Starting VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).

        :default: 8
        '''
        result = self._values.get("compute_environment_desired_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compute_environment_egress_cidr_blocks(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR blocks to which egress is allowed from the Batch Compute environment's security group.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("compute_environment_egress_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def compute_environment_instance_types(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The instance types for the compute environment.

        :default: c4.large,c4.xlarge,c4.2xlarge,c4.4xlarge,c4.8xlarge
        '''
        result = self._values.get("compute_environment_instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def compute_environment_max_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Maximum VCPUs for Batch Compute Environment [16-96].

        :default: 64
        '''
        result = self._values.get("compute_environment_max_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compute_environment_min_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Minimum VCPUs for Batch Compute Environment [0-16] for EC2 Batch Compute Environment (ignored for Fargate).

        :default: 8
        '''
        result = self._values.get("compute_environment_min_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_custom_batch_container_registry(self) -> typing.Optional[builtins.bool]:
        '''Provisions infrastructure for custom Amazon ECR container registry if enabled.'''
        result = self._values.get("enable_custom_batch_container_registry")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_ui_backend_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables for UI backend container.

        :default:

        [object Object]
        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("extra_ui_backend_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def extra_ui_static_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables for UI static app.

        :default:

        [object Object]
        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("extra_ui_static_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def force_destroy_s3_bucket(self) -> typing.Optional[builtins.bool]:
        '''Empty S3 bucket before destroying via terraform destroy.'''
        result = self._values.get("force_destroy_s3_bucket")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_partition(self) -> typing.Optional[builtins.str]:
        '''IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is).

        :default: aws
        '''
        result = self._values.get("iam_partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_http_endpoint(self) -> typing.Optional[builtins.str]:
        '''Whether the metadata service is available.

        Can be 'enabled' or 'disabled'

        :default: enabled
        '''
        result = self._values.get("launch_template_http_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_template_http_put_response_hop_limit(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The desired HTTP PUT response hop limit for instance metadata requests.

        Can be an integer from 1 to 64

        :default: 2
        '''
        result = self._values.get("launch_template_http_put_response_hop_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def launch_template_http_tokens(self) -> typing.Optional[builtins.str]:
        '''Whether or not the metadata service requires session tokens, also referred to as Instance Metadata Service Version 2 (IMDSv2).

        Can be 'optional' or 'required'

        :default: optional
        '''
        result = self._values.get("launch_template_http_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_service_container_image(self) -> typing.Optional[builtins.str]:
        '''Container image for metadata service.'''
        result = self._values.get("metadata_service_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_service_enable_api_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable basic auth for API Gateway?

        (requires key export)

        :default: true
        '''
        result = self._values.get("metadata_service_enable_api_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metadata_service_enable_api_gateway(self) -> typing.Optional[builtins.bool]:
        '''Enable API Gateway for public metadata service endpoint.

        :default: true
        '''
        result = self._values.get("metadata_service_enable_api_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def resource_prefix(self) -> typing.Any:
        '''string prefix for all resources.

        :default: metaflow
        '''
        result = self._values.get("resource_prefix")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_suffix(self) -> typing.Any:
        '''string suffix for all resources.'''
        result = self._values.get("resource_suffix")
        return typing.cast(typing.Any, result)

    @builtins.property
    def ui_alb_internal(self) -> typing.Optional[builtins.bool]:
        '''Defines whether the ALB for the UI is internal.'''
        result = self._values.get("ui_alb_internal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ui_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CIDRs we want to grant access to our Metaflow UI Service.

        Usually this is our VPN's CIDR blocks.
        '''
        result = self._values.get("ui_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ui_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''SSL certificate for UI.

        If set to empty string, UI is disabled.
        '''
        result = self._values.get("ui_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ui_static_container_image(self) -> typing.Optional[builtins.str]:
        '''Container image for the UI frontend app.'''
        result = self._values.get("ui_static_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowDatastore(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowDatastore",
):
    '''Defines an MetaflowDatastore based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/datastore outerbounds/metaflow/aws//modules/datastore}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        metadata_service_security_group_id: builtins.str,
        metaflow_vpc_id: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        db_engine: typing.Optional[builtins.str] = None,
        db_engine_version: typing.Optional[builtins.str] = None,
        db_instance_type: typing.Optional[builtins.str] = None,
        db_name: typing.Optional[builtins.str] = None,
        db_username: typing.Optional[builtins.str] = None,
        force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param metadata_service_security_group_id: The security group ID used by the MetaData service. We'll grant this access to our DB.
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First subnet used for availability zone redundancy.
        :param subnet2_id: Second subnet used for availability zone redundancy.
        :param db_engine: undefined. Default: postgres
        :param db_engine_version: undefined. Default: 11
        :param db_instance_type: RDS instance type to launch for PostgresQL database. Default: db.t2.small
        :param db_name: Name of PostgresQL database for Metaflow service. Default: metaflow
        :param db_username: PostgresQL username; defaults to 'metaflow' Default: metaflow
        :param force_destroy_s3_bucket: Empty S3 bucket before destroying via terraform destroy.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6211efd6f48fadd33fe149c71d77f56745e949d7c1ecc68d62e84e4e5d215e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowDatastoreConfig(
            metadata_service_security_group_id=metadata_service_security_group_id,
            metaflow_vpc_id=metaflow_vpc_id,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            standard_tags=standard_tags,
            subnet1_id=subnet1_id,
            subnet2_id=subnet2_id,
            db_engine=db_engine,
            db_engine_version=db_engine_version,
            db_instance_type=db_instance_type,
            db_name=db_name,
            db_username=db_username,
            force_destroy_s3_bucket=force_destroy_s3_bucket,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="databaseNameOutput")
    def database_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="databasePasswordOutput")
    def database_password_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databasePasswordOutput"))

    @builtins.property
    @jsii.member(jsii_name="databaseUsernameOutput")
    def database_username_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseUsernameOutput"))

    @builtins.property
    @jsii.member(jsii_name="datastoreS3BucketKmsKeyArnOutput")
    def datastore_s3_bucket_kms_key_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastoreS3BucketKmsKeyArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowDatastoreSysrootS3Output")
    def metaflow_datastore_sysroot_s3_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowDatastoreSysrootS3Output"))

    @builtins.property
    @jsii.member(jsii_name="metaflowDatatoolsS3RootOutput")
    def metaflow_datatools_s3_root_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowDatatoolsS3RootOutput"))

    @builtins.property
    @jsii.member(jsii_name="rdsMasterInstanceEndpointOutput")
    def rds_master_instance_endpoint_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdsMasterInstanceEndpointOutput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketArnOutput")
    def s3_bucket_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameOutput")
    def s3_bucket_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="metadataServiceSecurityGroupId")
    def metadata_service_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataServiceSecurityGroupId"))

    @metadata_service_security_group_id.setter
    def metadata_service_security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ad2e4372074cd8fbdf74746941e608370389038e220cf960efd2cd82afceb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceSecurityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="metaflowVpcId")
    def metaflow_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowVpcId"))

    @metaflow_vpc_id.setter
    def metaflow_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d5d4490bef28bf5250debe48e1b318ce0c0ea372801288a7e65a8da0319989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metaflowVpcId", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510cc062fc31c1397a4fa1196e5209c58ad5f2ad7dab8d7ec09f302d15ffb795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b23e041919ee471ed3ab82c932ee018458cb307209604da9819feed6266087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="standardTags")
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "standardTags"))

    @standard_tags.setter
    def standard_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e71912e31dfc49dedf411886c3ced0707524e8c1346c8eddc4a2199a74ad5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardTags", value)

    @builtins.property
    @jsii.member(jsii_name="subnet1Id")
    def subnet1_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet1Id"))

    @subnet1_id.setter
    def subnet1_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb5467e0db60879b57c05ddb1ba73c99e588b90ec6267ed7351841561298da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet1Id", value)

    @builtins.property
    @jsii.member(jsii_name="subnet2Id")
    def subnet2_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet2Id"))

    @subnet2_id.setter
    def subnet2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e5d713366e5074a307bf00f159e0f7f93939b5fc4cc2e2f3d17a091a299507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet2Id", value)

    @builtins.property
    @jsii.member(jsii_name="dbEngine")
    def db_engine(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbEngine"))

    @db_engine.setter
    def db_engine(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c48c8ec5aa5bae49ba4b74b630e87ca797173c8d904f2105c0f4d098686993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbEngine", value)

    @builtins.property
    @jsii.member(jsii_name="dbEngineVersion")
    def db_engine_version(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbEngineVersion"))

    @db_engine_version.setter
    def db_engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c1cef82f0bb29d3978522e75f6bc9a6ed488ddcb38d2427cebf9b14b773d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbEngineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceType")
    def db_instance_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbInstanceType"))

    @db_instance_type.setter
    def db_instance_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e043cbc9aa4b915e2e06af4fb9a28cb48a8fa8b9674f450c7c8653022474197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbInstanceType", value)

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbName"))

    @db_name.setter
    def db_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a58f7fdf31431db9e44fc3d1539eb341fe02ca965590c8a0c791ed3b1607ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbName", value)

    @builtins.property
    @jsii.member(jsii_name="dbUsername")
    def db_username(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbUsername"))

    @db_username.setter
    def db_username(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b30e9057d5a3b05c91390d9843aaa08d298e7e1583af48b661bb9ec79b2964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbUsername", value)

    @builtins.property
    @jsii.member(jsii_name="forceDestroyS3Bucket")
    def force_destroy_s3_bucket(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "forceDestroyS3Bucket"))

    @force_destroy_s3_bucket.setter
    def force_destroy_s3_bucket(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e9ecdfbd4ed97e253ba9bdb13379c80a40d61b1ca453aac0c25d9fb264c9de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroyS3Bucket", value)


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowDatastoreConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "metadata_service_security_group_id": "metadataServiceSecurityGroupId",
        "metaflow_vpc_id": "metaflowVpcId",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "standard_tags": "standardTags",
        "subnet1_id": "subnet1Id",
        "subnet2_id": "subnet2Id",
        "db_engine": "dbEngine",
        "db_engine_version": "dbEngineVersion",
        "db_instance_type": "dbInstanceType",
        "db_name": "dbName",
        "db_username": "dbUsername",
        "force_destroy_s3_bucket": "forceDestroyS3Bucket",
    },
)
class MetaflowDatastoreConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        metadata_service_security_group_id: builtins.str,
        metaflow_vpc_id: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        db_engine: typing.Optional[builtins.str] = None,
        db_engine_version: typing.Optional[builtins.str] = None,
        db_instance_type: typing.Optional[builtins.str] = None,
        db_name: typing.Optional[builtins.str] = None,
        db_username: typing.Optional[builtins.str] = None,
        force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param metadata_service_security_group_id: The security group ID used by the MetaData service. We'll grant this access to our DB.
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First subnet used for availability zone redundancy.
        :param subnet2_id: Second subnet used for availability zone redundancy.
        :param db_engine: undefined. Default: postgres
        :param db_engine_version: undefined. Default: 11
        :param db_instance_type: RDS instance type to launch for PostgresQL database. Default: db.t2.small
        :param db_name: Name of PostgresQL database for Metaflow service. Default: metaflow
        :param db_username: PostgresQL username; defaults to 'metaflow' Default: metaflow
        :param force_destroy_s3_bucket: Empty S3 bucket before destroying via terraform destroy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c4234a39f77d9aef76201cffcf80f6f8750d1b26600201ff54d15fbe36c3f8)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument metadata_service_security_group_id", value=metadata_service_security_group_id, expected_type=type_hints["metadata_service_security_group_id"])
            check_type(argname="argument metaflow_vpc_id", value=metaflow_vpc_id, expected_type=type_hints["metaflow_vpc_id"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument standard_tags", value=standard_tags, expected_type=type_hints["standard_tags"])
            check_type(argname="argument subnet1_id", value=subnet1_id, expected_type=type_hints["subnet1_id"])
            check_type(argname="argument subnet2_id", value=subnet2_id, expected_type=type_hints["subnet2_id"])
            check_type(argname="argument db_engine", value=db_engine, expected_type=type_hints["db_engine"])
            check_type(argname="argument db_engine_version", value=db_engine_version, expected_type=type_hints["db_engine_version"])
            check_type(argname="argument db_instance_type", value=db_instance_type, expected_type=type_hints["db_instance_type"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument db_username", value=db_username, expected_type=type_hints["db_username"])
            check_type(argname="argument force_destroy_s3_bucket", value=force_destroy_s3_bucket, expected_type=type_hints["force_destroy_s3_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_service_security_group_id": metadata_service_security_group_id,
            "metaflow_vpc_id": metaflow_vpc_id,
            "resource_prefix": resource_prefix,
            "resource_suffix": resource_suffix,
            "standard_tags": standard_tags,
            "subnet1_id": subnet1_id,
            "subnet2_id": subnet2_id,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if db_engine is not None:
            self._values["db_engine"] = db_engine
        if db_engine_version is not None:
            self._values["db_engine_version"] = db_engine_version
        if db_instance_type is not None:
            self._values["db_instance_type"] = db_instance_type
        if db_name is not None:
            self._values["db_name"] = db_name
        if db_username is not None:
            self._values["db_username"] = db_username
        if force_destroy_s3_bucket is not None:
            self._values["force_destroy_s3_bucket"] = force_destroy_s3_bucket

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metadata_service_security_group_id(self) -> builtins.str:
        '''The security group ID used by the MetaData service.

        We'll grant this access to our DB.
        '''
        result = self._values.get("metadata_service_security_group_id")
        assert result is not None, "Required property 'metadata_service_security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metaflow_vpc_id(self) -> builtins.str:
        '''ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.'''
        result = self._values.get("metaflow_vpc_id")
        assert result is not None, "Required property 'metaflow_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_prefix(self) -> builtins.str:
        '''Prefix given to all AWS resources to differentiate between applications.'''
        result = self._values.get("resource_prefix")
        assert result is not None, "Required property 'resource_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_suffix(self) -> builtins.str:
        '''Suffix given to all AWS resources to differentiate between environment and workspace.'''
        result = self._values.get("resource_suffix")
        assert result is not None, "Required property 'resource_suffix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The standard tags to apply to every AWS resource.

        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("standard_tags")
        assert result is not None, "Required property 'standard_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def subnet1_id(self) -> builtins.str:
        '''First subnet used for availability zone redundancy.'''
        result = self._values.get("subnet1_id")
        assert result is not None, "Required property 'subnet1_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet2_id(self) -> builtins.str:
        '''Second subnet used for availability zone redundancy.'''
        result = self._values.get("subnet2_id")
        assert result is not None, "Required property 'subnet2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_engine(self) -> typing.Optional[builtins.str]:
        '''undefined.

        :default: postgres
        '''
        result = self._values.get("db_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_engine_version(self) -> typing.Optional[builtins.str]:
        '''undefined.

        :default: 11
        '''
        result = self._values.get("db_engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_type(self) -> typing.Optional[builtins.str]:
        '''RDS instance type to launch for PostgresQL database.

        :default: db.t2.small
        '''
        result = self._values.get("db_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_name(self) -> typing.Optional[builtins.str]:
        '''Name of PostgresQL database for Metaflow service.

        :default: metaflow
        '''
        result = self._values.get("db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_username(self) -> typing.Optional[builtins.str]:
        '''PostgresQL username;

        defaults to 'metaflow'

        :default: metaflow
        '''
        result = self._values.get("db_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_destroy_s3_bucket(self) -> typing.Optional[builtins.bool]:
        '''Empty S3 bucket before destroying via terraform destroy.'''
        result = self._values.get("force_destroy_s3_bucket")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowDatastoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowMetadataService(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowMetadataService",
):
    '''Defines an MetaflowMetadataService based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/metadata-service outerbounds/metaflow/aws//modules/metadata-service}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_list_cidr_blocks: typing.Sequence[builtins.str],
        database_password: builtins.str,
        database_username: builtins.str,
        datastore_s3_bucket_kms_key_arn: builtins.str,
        fargate_execution_role_arn: builtins.str,
        metaflow_vpc_id: builtins.str,
        rds_master_instance_endpoint: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        vpc_cidr_blocks: typing.Sequence[builtins.str],
        with_public_ip: builtins.bool,
        database_name: typing.Optional[builtins.str] = None,
        enable_api_basic_auth: typing.Optional[builtins.bool] = None,
        enable_api_gateway: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        is_gov: typing.Optional[builtins.bool] = None,
        metadata_service_container_image: typing.Optional[builtins.str] = None,
        metadata_service_cpu: typing.Optional[jsii.Number] = None,
        metadata_service_memory: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_list_cidr_blocks: List of CIDRs we want to grant access to our Metaflow Metadata Service. Usually this is our VPN's CIDR blocks.
        :param database_password: The database password.
        :param database_username: The database username.
        :param datastore_s3_bucket_kms_key_arn: The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.
        :param fargate_execution_role_arn: The IAM role that grants access to ECS and Batch services which we'll use as our Metadata Service API's execution_role for our Fargate instance.
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param rds_master_instance_endpoint: The database connection endpoint in address:port format.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: The ARN of the bucket we'll be using as blob storage.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First private subnet used for availability zone redundancy.
        :param subnet2_id: Second private subnet used for availability zone redundancy.
        :param vpc_cidr_blocks: The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.
        :param with_public_ip: Enable public IP assignment for the Metadata Service. Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        :param database_name: The database name. Default: metaflow
        :param enable_api_basic_auth: Enable basic auth for API Gateway? (requires key export) Default: true
        :param enable_api_gateway: Enable API Gateway for public metadata service endpoint. Default: true
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param is_gov: Set to true if IAM partition is 'aws-us-gov'.
        :param metadata_service_container_image: Container image for metadata service.
        :param metadata_service_cpu: ECS task CPU unit for metadata service. Default: 512
        :param metadata_service_memory: ECS task memory in MiB for metadata service. Default: 1024
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a5684d135286dde8f18f1429942040c15944ae4768fe62e56efc200a74f200)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowMetadataServiceConfig(
            access_list_cidr_blocks=access_list_cidr_blocks,
            database_password=database_password,
            database_username=database_username,
            datastore_s3_bucket_kms_key_arn=datastore_s3_bucket_kms_key_arn,
            fargate_execution_role_arn=fargate_execution_role_arn,
            metaflow_vpc_id=metaflow_vpc_id,
            rds_master_instance_endpoint=rds_master_instance_endpoint,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            s3_bucket_arn=s3_bucket_arn,
            standard_tags=standard_tags,
            subnet1_id=subnet1_id,
            subnet2_id=subnet2_id,
            vpc_cidr_blocks=vpc_cidr_blocks,
            with_public_ip=with_public_ip,
            database_name=database_name,
            enable_api_basic_auth=enable_api_basic_auth,
            enable_api_gateway=enable_api_gateway,
            iam_partition=iam_partition,
            is_gov=is_gov,
            metadata_service_container_image=metadata_service_container_image,
            metadata_service_cpu=metadata_service_cpu,
            metadata_service_memory=metadata_service_memory,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRestApiIdKeyIdOutput")
    def api_gateway_rest_api_id_key_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGatewayRestApiIdKeyIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRestApiIdOutput")
    def api_gateway_rest_api_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiGatewayRestApiIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="metadataServiceSecurityGroupIdOutput")
    def metadata_service_security_group_id_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataServiceSecurityGroupIdOutput"))

    @builtins.property
    @jsii.member(jsii_name="metadataSvcEcsTaskRoleArnOutput")
    def metadata_svc_ecs_task_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataSvcEcsTaskRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowServiceInternalUrlOutput")
    def metaflow_service_internal_url_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowServiceInternalUrlOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowServiceUrlOutput")
    def metaflow_service_url_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowServiceUrlOutput"))

    @builtins.property
    @jsii.member(jsii_name="migrationFunctionArnOutput")
    def migration_function_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "migrationFunctionArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="networkLoadBalancerDnsNameOutput")
    def network_load_balancer_dns_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkLoadBalancerDnsNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="accessListCidrBlocks")
    def access_list_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessListCidrBlocks"))

    @access_list_cidr_blocks.setter
    def access_list_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177ba7546a8a3c8052b7177f00dc008db8de159be8527166073bab19b3401c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessListCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="databasePassword")
    def database_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databasePassword"))

    @database_password.setter
    def database_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0e4fe919decd061264a28cb3357c372b21d6d7b82cf9b92ff53e162af49534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databasePassword", value)

    @builtins.property
    @jsii.member(jsii_name="databaseUsername")
    def database_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseUsername"))

    @database_username.setter
    def database_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474b52ff7f03d32e140a0664ddf608ae1c30cb557558f89eec7a1b01744b9952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseUsername", value)

    @builtins.property
    @jsii.member(jsii_name="datastoreS3BucketKmsKeyArn")
    def datastore_s3_bucket_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastoreS3BucketKmsKeyArn"))

    @datastore_s3_bucket_kms_key_arn.setter
    def datastore_s3_bucket_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7138b0f8867684ff60462fca6129b805183bf3f2aa2dd40377a2daa0857f99c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastoreS3BucketKmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="fargateExecutionRoleArn")
    def fargate_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fargateExecutionRoleArn"))

    @fargate_execution_role_arn.setter
    def fargate_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e8604fe768f188c267aa732f99bd8ee8e4a3ae9910e0d828bf989a29a86e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fargateExecutionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="metaflowVpcId")
    def metaflow_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowVpcId"))

    @metaflow_vpc_id.setter
    def metaflow_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7984f06df03fc9c5263efd600d0a6c9121d80467da55fb020230a351cfc170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metaflowVpcId", value)

    @builtins.property
    @jsii.member(jsii_name="rdsMasterInstanceEndpoint")
    def rds_master_instance_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdsMasterInstanceEndpoint"))

    @rds_master_instance_endpoint.setter
    def rds_master_instance_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9c829b7203dce2629a0248654455e3212476465f04b8b820f77ca00eac78a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdsMasterInstanceEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604aa7780d3092325295cdbdbfac5ad5051dd6415ed6ad613bc9ec20cdd018f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bce855b9373ae829f83a95498f9f228e400614fd6f866823ec24a123ee17cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArn"))

    @s3_bucket_arn.setter
    def s3_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d9df2c5fcd68ca6a8ce730ec192777f253900cc95abdbea3c83b7ddfc3513a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="standardTags")
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "standardTags"))

    @standard_tags.setter
    def standard_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c120ad64f66a5b4271f1a34a292ff49dca70e405f53f621bd3d7a08511d6732b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardTags", value)

    @builtins.property
    @jsii.member(jsii_name="subnet1Id")
    def subnet1_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet1Id"))

    @subnet1_id.setter
    def subnet1_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff5de91741a05a222c5d31809a2970561c1727003febfac6040d466f24852c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet1Id", value)

    @builtins.property
    @jsii.member(jsii_name="subnet2Id")
    def subnet2_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet2Id"))

    @subnet2_id.setter
    def subnet2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafb6d9f85e432e4ba67c33d85dc77267445c3df672a5d312cebaa7ed1519fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet2Id", value)

    @builtins.property
    @jsii.member(jsii_name="vpcCidrBlocks")
    def vpc_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcCidrBlocks"))

    @vpc_cidr_blocks.setter
    def vpc_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0680e3170408a6718d3b6e34bafb9c1fa0f581619badc079f4326a286d6e6c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="withPublicIp")
    def with_public_ip(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "withPublicIp"))

    @with_public_ip.setter
    def with_public_ip(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1228cba52ba2f1a47f0a02dbfc3a16e562b13a237640721aad2bb8bd6f01e53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a18b3d3dff6a35a21ec14ce7e0f2de207879ca380d1c6f4ff266b60c571ed21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="enableApiBasicAuth")
    def enable_api_basic_auth(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableApiBasicAuth"))

    @enable_api_basic_auth.setter
    def enable_api_basic_auth(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcafdac999ad6971d5956edc302564c5d9fab945a2284c866c1d2318aa30889d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApiBasicAuth", value)

    @builtins.property
    @jsii.member(jsii_name="enableApiGateway")
    def enable_api_gateway(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableApiGateway"))

    @enable_api_gateway.setter
    def enable_api_gateway(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9945e95e0b67e0de746c3f554642536ed64bcd47c96c2592a848013bef6483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableApiGateway", value)

    @builtins.property
    @jsii.member(jsii_name="iamPartition")
    def iam_partition(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamPartition"))

    @iam_partition.setter
    def iam_partition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a8b90ad5580e42b9b600cd8ee832cc9f8776edb5e0ebbd1e66770484e2d479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPartition", value)

    @builtins.property
    @jsii.member(jsii_name="isGov")
    def is_gov(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isGov"))

    @is_gov.setter
    def is_gov(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c571d34d2187c67c2e813249c279cbb433561eeaeaaae9f10f56afeb894774f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isGov", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceContainerImage")
    def metadata_service_container_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataServiceContainerImage"))

    @metadata_service_container_image.setter
    def metadata_service_container_image(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc9ee5e9f85cc93de30ec3f703572f339ab432c0b382e28f844b4b672c7b688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceContainerImage", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceCpu")
    def metadata_service_cpu(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metadataServiceCpu"))

    @metadata_service_cpu.setter
    def metadata_service_cpu(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a611b11fa101496188393844d016894c5d503f47cca6b53ae12d0b0514987f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceCpu", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceMemory")
    def metadata_service_memory(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metadataServiceMemory"))

    @metadata_service_memory.setter
    def metadata_service_memory(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fca6d4146676b2adec57f9a725d309cd1b48d7adaeffefead221b13f366abb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceMemory", value)


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowMetadataServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "access_list_cidr_blocks": "accessListCidrBlocks",
        "database_password": "databasePassword",
        "database_username": "databaseUsername",
        "datastore_s3_bucket_kms_key_arn": "datastoreS3BucketKmsKeyArn",
        "fargate_execution_role_arn": "fargateExecutionRoleArn",
        "metaflow_vpc_id": "metaflowVpcId",
        "rds_master_instance_endpoint": "rdsMasterInstanceEndpoint",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "s3_bucket_arn": "s3BucketArn",
        "standard_tags": "standardTags",
        "subnet1_id": "subnet1Id",
        "subnet2_id": "subnet2Id",
        "vpc_cidr_blocks": "vpcCidrBlocks",
        "with_public_ip": "withPublicIp",
        "database_name": "databaseName",
        "enable_api_basic_auth": "enableApiBasicAuth",
        "enable_api_gateway": "enableApiGateway",
        "iam_partition": "iamPartition",
        "is_gov": "isGov",
        "metadata_service_container_image": "metadataServiceContainerImage",
        "metadata_service_cpu": "metadataServiceCpu",
        "metadata_service_memory": "metadataServiceMemory",
    },
)
class MetaflowMetadataServiceConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        access_list_cidr_blocks: typing.Sequence[builtins.str],
        database_password: builtins.str,
        database_username: builtins.str,
        datastore_s3_bucket_kms_key_arn: builtins.str,
        fargate_execution_role_arn: builtins.str,
        metaflow_vpc_id: builtins.str,
        rds_master_instance_endpoint: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        vpc_cidr_blocks: typing.Sequence[builtins.str],
        with_public_ip: builtins.bool,
        database_name: typing.Optional[builtins.str] = None,
        enable_api_basic_auth: typing.Optional[builtins.bool] = None,
        enable_api_gateway: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        is_gov: typing.Optional[builtins.bool] = None,
        metadata_service_container_image: typing.Optional[builtins.str] = None,
        metadata_service_cpu: typing.Optional[jsii.Number] = None,
        metadata_service_memory: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param access_list_cidr_blocks: List of CIDRs we want to grant access to our Metaflow Metadata Service. Usually this is our VPN's CIDR blocks.
        :param database_password: The database password.
        :param database_username: The database username.
        :param datastore_s3_bucket_kms_key_arn: The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.
        :param fargate_execution_role_arn: The IAM role that grants access to ECS and Batch services which we'll use as our Metadata Service API's execution_role for our Fargate instance.
        :param metaflow_vpc_id: ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.
        :param rds_master_instance_endpoint: The database connection endpoint in address:port format.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: The ARN of the bucket we'll be using as blob storage.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First private subnet used for availability zone redundancy.
        :param subnet2_id: Second private subnet used for availability zone redundancy.
        :param vpc_cidr_blocks: The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.
        :param with_public_ip: Enable public IP assignment for the Metadata Service. Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        :param database_name: The database name. Default: metaflow
        :param enable_api_basic_auth: Enable basic auth for API Gateway? (requires key export) Default: true
        :param enable_api_gateway: Enable API Gateway for public metadata service endpoint. Default: true
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param is_gov: Set to true if IAM partition is 'aws-us-gov'.
        :param metadata_service_container_image: Container image for metadata service.
        :param metadata_service_cpu: ECS task CPU unit for metadata service. Default: 512
        :param metadata_service_memory: ECS task memory in MiB for metadata service. Default: 1024
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d87e5f7076de12631af86993934ec6cb65adc08c125543b3bc9e7b29929dacc)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument access_list_cidr_blocks", value=access_list_cidr_blocks, expected_type=type_hints["access_list_cidr_blocks"])
            check_type(argname="argument database_password", value=database_password, expected_type=type_hints["database_password"])
            check_type(argname="argument database_username", value=database_username, expected_type=type_hints["database_username"])
            check_type(argname="argument datastore_s3_bucket_kms_key_arn", value=datastore_s3_bucket_kms_key_arn, expected_type=type_hints["datastore_s3_bucket_kms_key_arn"])
            check_type(argname="argument fargate_execution_role_arn", value=fargate_execution_role_arn, expected_type=type_hints["fargate_execution_role_arn"])
            check_type(argname="argument metaflow_vpc_id", value=metaflow_vpc_id, expected_type=type_hints["metaflow_vpc_id"])
            check_type(argname="argument rds_master_instance_endpoint", value=rds_master_instance_endpoint, expected_type=type_hints["rds_master_instance_endpoint"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument standard_tags", value=standard_tags, expected_type=type_hints["standard_tags"])
            check_type(argname="argument subnet1_id", value=subnet1_id, expected_type=type_hints["subnet1_id"])
            check_type(argname="argument subnet2_id", value=subnet2_id, expected_type=type_hints["subnet2_id"])
            check_type(argname="argument vpc_cidr_blocks", value=vpc_cidr_blocks, expected_type=type_hints["vpc_cidr_blocks"])
            check_type(argname="argument with_public_ip", value=with_public_ip, expected_type=type_hints["with_public_ip"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument enable_api_basic_auth", value=enable_api_basic_auth, expected_type=type_hints["enable_api_basic_auth"])
            check_type(argname="argument enable_api_gateway", value=enable_api_gateway, expected_type=type_hints["enable_api_gateway"])
            check_type(argname="argument iam_partition", value=iam_partition, expected_type=type_hints["iam_partition"])
            check_type(argname="argument is_gov", value=is_gov, expected_type=type_hints["is_gov"])
            check_type(argname="argument metadata_service_container_image", value=metadata_service_container_image, expected_type=type_hints["metadata_service_container_image"])
            check_type(argname="argument metadata_service_cpu", value=metadata_service_cpu, expected_type=type_hints["metadata_service_cpu"])
            check_type(argname="argument metadata_service_memory", value=metadata_service_memory, expected_type=type_hints["metadata_service_memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_list_cidr_blocks": access_list_cidr_blocks,
            "database_password": database_password,
            "database_username": database_username,
            "datastore_s3_bucket_kms_key_arn": datastore_s3_bucket_kms_key_arn,
            "fargate_execution_role_arn": fargate_execution_role_arn,
            "metaflow_vpc_id": metaflow_vpc_id,
            "rds_master_instance_endpoint": rds_master_instance_endpoint,
            "resource_prefix": resource_prefix,
            "resource_suffix": resource_suffix,
            "s3_bucket_arn": s3_bucket_arn,
            "standard_tags": standard_tags,
            "subnet1_id": subnet1_id,
            "subnet2_id": subnet2_id,
            "vpc_cidr_blocks": vpc_cidr_blocks,
            "with_public_ip": with_public_ip,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if database_name is not None:
            self._values["database_name"] = database_name
        if enable_api_basic_auth is not None:
            self._values["enable_api_basic_auth"] = enable_api_basic_auth
        if enable_api_gateway is not None:
            self._values["enable_api_gateway"] = enable_api_gateway
        if iam_partition is not None:
            self._values["iam_partition"] = iam_partition
        if is_gov is not None:
            self._values["is_gov"] = is_gov
        if metadata_service_container_image is not None:
            self._values["metadata_service_container_image"] = metadata_service_container_image
        if metadata_service_cpu is not None:
            self._values["metadata_service_cpu"] = metadata_service_cpu
        if metadata_service_memory is not None:
            self._values["metadata_service_memory"] = metadata_service_memory

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def access_list_cidr_blocks(self) -> typing.List[builtins.str]:
        '''List of CIDRs we want to grant access to our Metaflow Metadata Service.

        Usually this is our VPN's CIDR blocks.
        '''
        result = self._values.get("access_list_cidr_blocks")
        assert result is not None, "Required property 'access_list_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def database_password(self) -> builtins.str:
        '''The database password.'''
        result = self._values.get("database_password")
        assert result is not None, "Required property 'database_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_username(self) -> builtins.str:
        '''The database username.'''
        result = self._values.get("database_username")
        assert result is not None, "Required property 'database_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore_s3_bucket_kms_key_arn(self) -> builtins.str:
        '''The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.'''
        result = self._values.get("datastore_s3_bucket_kms_key_arn")
        assert result is not None, "Required property 'datastore_s3_bucket_kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fargate_execution_role_arn(self) -> builtins.str:
        '''The IAM role that grants access to ECS and Batch services which we'll use as our Metadata Service API's execution_role for our Fargate instance.'''
        result = self._values.get("fargate_execution_role_arn")
        assert result is not None, "Required property 'fargate_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metaflow_vpc_id(self) -> builtins.str:
        '''ID of the Metaflow VPC this SageMaker notebook instance is to be deployed in.'''
        result = self._values.get("metaflow_vpc_id")
        assert result is not None, "Required property 'metaflow_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_master_instance_endpoint(self) -> builtins.str:
        '''The database connection endpoint in address:port format.'''
        result = self._values.get("rds_master_instance_endpoint")
        assert result is not None, "Required property 'rds_master_instance_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_prefix(self) -> builtins.str:
        '''Prefix given to all AWS resources to differentiate between applications.'''
        result = self._values.get("resource_prefix")
        assert result is not None, "Required property 'resource_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_suffix(self) -> builtins.str:
        '''Suffix given to all AWS resources to differentiate between environment and workspace.'''
        result = self._values.get("resource_suffix")
        assert result is not None, "Required property 'resource_suffix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_arn(self) -> builtins.str:
        '''The ARN of the bucket we'll be using as blob storage.'''
        result = self._values.get("s3_bucket_arn")
        assert result is not None, "Required property 's3_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The standard tags to apply to every AWS resource.

        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("standard_tags")
        assert result is not None, "Required property 'standard_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def subnet1_id(self) -> builtins.str:
        '''First private subnet used for availability zone redundancy.'''
        result = self._values.get("subnet1_id")
        assert result is not None, "Required property 'subnet1_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet2_id(self) -> builtins.str:
        '''Second private subnet used for availability zone redundancy.'''
        result = self._values.get("subnet2_id")
        assert result is not None, "Required property 'subnet2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_cidr_blocks(self) -> typing.List[builtins.str]:
        '''The VPC CIDR blocks that we'll access list on our Metadata Service API to allow all internal communications.'''
        result = self._values.get("vpc_cidr_blocks")
        assert result is not None, "Required property 'vpc_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def with_public_ip(self) -> builtins.bool:
        '''Enable public IP assignment for the Metadata Service.

        Typically you want this to be set to true if using public subnets as subnet1_id and subnet2_id, and false otherwise
        '''
        result = self._values.get("with_public_ip")
        assert result is not None, "Required property 'with_public_ip' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The database name.

        :default: metaflow
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_api_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''Enable basic auth for API Gateway?

        (requires key export)

        :default: true
        '''
        result = self._values.get("enable_api_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_api_gateway(self) -> typing.Optional[builtins.bool]:
        '''Enable API Gateway for public metadata service endpoint.

        :default: true
        '''
        result = self._values.get("enable_api_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_partition(self) -> typing.Optional[builtins.str]:
        '''IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is).

        :default: aws
        '''
        result = self._values.get("iam_partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_gov(self) -> typing.Optional[builtins.bool]:
        '''Set to true if IAM partition is 'aws-us-gov'.'''
        result = self._values.get("is_gov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metadata_service_container_image(self) -> typing.Optional[builtins.str]:
        '''Container image for metadata service.'''
        result = self._values.get("metadata_service_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_service_cpu(self) -> typing.Optional[jsii.Number]:
        '''ECS task CPU unit for metadata service.

        :default: 512
        '''
        result = self._values.get("metadata_service_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metadata_service_memory(self) -> typing.Optional[jsii.Number]:
        '''ECS task memory in MiB for metadata service.

        :default: 1024
        '''
        result = self._values.get("metadata_service_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowMetadataServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowStepFunctions(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowStepFunctions",
):
    '''Defines an MetaflowStepFunctions based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/step-functions outerbounds/metaflow/aws//modules/step-functions}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        batch_job_queue_arn: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        s3_bucket_kms_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        active: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param batch_job_queue_arn: Batch job queue arn.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: arn of the metaflow datastore s3 bucket.
        :param s3_bucket_kms_arn: arn of the metaflow datastore s3 bucket's kms key.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param active: When true step function infrastructure is provisioned.
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0bf7a24bd4485357457ded48e181f9e0173a7df7f7e9b463cebdcd02479cce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowStepFunctionsConfig(
            batch_job_queue_arn=batch_job_queue_arn,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            s3_bucket_arn=s3_bucket_arn,
            s3_bucket_kms_arn=s3_bucket_kms_arn,
            standard_tags=standard_tags,
            active=active,
            iam_partition=iam_partition,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="metaflowEventbridgeRoleArnOutput")
    def metaflow_eventbridge_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowEventbridgeRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowStepFunctionsDynamodbPolicyOutput")
    def metaflow_step_functions_dynamodb_policy_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowStepFunctionsDynamodbPolicyOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowStepFunctionsDynamodbTableArnOutput")
    def metaflow_step_functions_dynamodb_table_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowStepFunctionsDynamodbTableArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowStepFunctionsDynamodbTableNameOutput")
    def metaflow_step_functions_dynamodb_table_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowStepFunctionsDynamodbTableNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="metaflowStepFunctionsRoleArnOutput")
    def metaflow_step_functions_role_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowStepFunctionsRoleArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="batchJobQueueArn")
    def batch_job_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchJobQueueArn"))

    @batch_job_queue_arn.setter
    def batch_job_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25fddf5fdf481b8466eeae5fb5d73962a617af6d875a6d10c394b97ab58ce24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchJobQueueArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9242d50a36034e44266cace376bbb4745c9d650b53664806909fe159dba00b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1c020ac6f73d1ed5076f4473957720420af4e3e012eea0a71f5e1f8712bde2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArn"))

    @s3_bucket_arn.setter
    def s3_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae71cf2850b010ef03283211ddc1a08e6aa6b560024d95f5a6ccb38e9e3b1441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketKmsArn")
    def s3_bucket_kms_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketKmsArn"))

    @s3_bucket_kms_arn.setter
    def s3_bucket_kms_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e86669da1bd161caf6c2e64713d818918439c6850e47f7e29a3701e14b98ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketKmsArn", value)

    @builtins.property
    @jsii.member(jsii_name="standardTags")
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "standardTags"))

    @standard_tags.setter
    def standard_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ebefe46f560ea7cf518e20d243517210896e8588c5fab179c5872c863613ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardTags", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "active"))

    @active.setter
    def active(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7effed9e5832f1c1eb68d176d4787369c06bf7492507837babc71c9283710bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="iamPartition")
    def iam_partition(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamPartition"))

    @iam_partition.setter
    def iam_partition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa186e83bdba71785915a8de994799016a90dba2e6f394d511e2d986ad88e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPartition", value)


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowStepFunctionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "batch_job_queue_arn": "batchJobQueueArn",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "s3_bucket_arn": "s3BucketArn",
        "s3_bucket_kms_arn": "s3BucketKmsArn",
        "standard_tags": "standardTags",
        "active": "active",
        "iam_partition": "iamPartition",
    },
)
class MetaflowStepFunctionsConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        batch_job_queue_arn: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        s3_bucket_kms_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        active: typing.Optional[builtins.bool] = None,
        iam_partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param batch_job_queue_arn: Batch job queue arn.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: arn of the metaflow datastore s3 bucket.
        :param s3_bucket_kms_arn: arn of the metaflow datastore s3 bucket's kms key.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param active: When true step function infrastructure is provisioned.
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2a2ba9ab32f59f0ffc89f0f30266bfc363285642496442ad7559da77da2e16)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument batch_job_queue_arn", value=batch_job_queue_arn, expected_type=type_hints["batch_job_queue_arn"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument s3_bucket_kms_arn", value=s3_bucket_kms_arn, expected_type=type_hints["s3_bucket_kms_arn"])
            check_type(argname="argument standard_tags", value=standard_tags, expected_type=type_hints["standard_tags"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument iam_partition", value=iam_partition, expected_type=type_hints["iam_partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "batch_job_queue_arn": batch_job_queue_arn,
            "resource_prefix": resource_prefix,
            "resource_suffix": resource_suffix,
            "s3_bucket_arn": s3_bucket_arn,
            "s3_bucket_kms_arn": s3_bucket_kms_arn,
            "standard_tags": standard_tags,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if active is not None:
            self._values["active"] = active
        if iam_partition is not None:
            self._values["iam_partition"] = iam_partition

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def batch_job_queue_arn(self) -> builtins.str:
        '''Batch job queue arn.'''
        result = self._values.get("batch_job_queue_arn")
        assert result is not None, "Required property 'batch_job_queue_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_prefix(self) -> builtins.str:
        '''Prefix given to all AWS resources to differentiate between applications.'''
        result = self._values.get("resource_prefix")
        assert result is not None, "Required property 'resource_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_suffix(self) -> builtins.str:
        '''Suffix given to all AWS resources to differentiate between environment and workspace.'''
        result = self._values.get("resource_suffix")
        assert result is not None, "Required property 'resource_suffix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_arn(self) -> builtins.str:
        '''arn of the metaflow datastore s3 bucket.'''
        result = self._values.get("s3_bucket_arn")
        assert result is not None, "Required property 's3_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_kms_arn(self) -> builtins.str:
        '''arn of the metaflow datastore s3 bucket's kms key.'''
        result = self._values.get("s3_bucket_kms_arn")
        assert result is not None, "Required property 's3_bucket_kms_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The standard tags to apply to every AWS resource.

        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("standard_tags")
        assert result is not None, "Required property 'standard_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def active(self) -> typing.Optional[builtins.bool]:
        '''When true step function infrastructure is provisioned.'''
        result = self._values.get("active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_partition(self) -> typing.Optional[builtins.str]:
        '''IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is).

        :default: aws
        '''
        result = self._values.get("iam_partition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowStepFunctionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowUi(
    _cdktf_9a9027ec.TerraformModule,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-metaflow-aws.MetaflowUi",
):
    '''Defines an MetaflowUi based on a Terraform module.

    Docs at Terraform Registry: {@link https://registry.terraform.io/modules/outerbounds/metaflow/aws/~> 0.9.4/submodules/ui outerbounds/metaflow/aws//modules/ui}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate_arn: builtins.str,
        database_password: builtins.str,
        database_username: builtins.str,
        datastore_s3_bucket_kms_key_arn: builtins.str,
        fargate_execution_role_arn: builtins.str,
        metadata_service_security_group_id: builtins.str,
        metaflow_datastore_sysroot_s3: builtins.str,
        metaflow_vpc_id: builtins.str,
        rds_master_instance_endpoint: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        alb_internal: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        is_gov: typing.Optional[builtins.bool] = None,
        ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_backend_container_image: typing.Optional[builtins.str] = None,
        ui_static_container_image: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param certificate_arn: SSL certificate ARN. The certificate will be used by the UI load balancer.
        :param database_password: The database password.
        :param database_username: The database username.
        :param datastore_s3_bucket_kms_key_arn: The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.
        :param fargate_execution_role_arn: This role allows Fargate to pull container images and logs. We'll use it as execution_role for our Fargate task
        :param metadata_service_security_group_id: The security group ID used by the MetaData service. This security group should allow connections to the RDS instance.
        :param metaflow_datastore_sysroot_s3: METAFLOW_DATASTORE_SYSROOT_S3 value.
        :param metaflow_vpc_id: VPC to deploy services into.
        :param rds_master_instance_endpoint: The database connection endpoint in address:port format.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: The ARN of the bucket used for Metaflow datastore.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First private subnet used for availability zone redundancy.
        :param subnet2_id: Second private subnet used for availability zone redundancy.
        :param alb_internal: Defines whether the ALB is internal.
        :param database_name: The database name. Default: metaflow
        :param extra_ui_backend_env_vars: Additional environment variables for UI backend container. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param extra_ui_static_env_vars: Additional environment variables for UI static app. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param is_gov: Set to true if IAM partition is 'aws-us-gov'.
        :param ui_allow_list: A list of CIDRs the UI will be available to.
        :param ui_backend_container_image: Container image for UI backend.
        :param ui_static_container_image: Container image for the UI frontend app.
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de8555760d621a1ce7c7248af48f7343ef0a843ed23f412c163d01dcdadf88e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = MetaflowUiConfig(
            certificate_arn=certificate_arn,
            database_password=database_password,
            database_username=database_username,
            datastore_s3_bucket_kms_key_arn=datastore_s3_bucket_kms_key_arn,
            fargate_execution_role_arn=fargate_execution_role_arn,
            metadata_service_security_group_id=metadata_service_security_group_id,
            metaflow_datastore_sysroot_s3=metaflow_datastore_sysroot_s3,
            metaflow_vpc_id=metaflow_vpc_id,
            rds_master_instance_endpoint=rds_master_instance_endpoint,
            resource_prefix=resource_prefix,
            resource_suffix=resource_suffix,
            s3_bucket_arn=s3_bucket_arn,
            standard_tags=standard_tags,
            subnet1_id=subnet1_id,
            subnet2_id=subnet2_id,
            alb_internal=alb_internal,
            database_name=database_name,
            extra_ui_backend_env_vars=extra_ui_backend_env_vars,
            extra_ui_static_env_vars=extra_ui_static_env_vars,
            iam_partition=iam_partition,
            is_gov=is_gov,
            ui_allow_list=ui_allow_list,
            ui_backend_container_image=ui_backend_container_image,
            ui_static_container_image=ui_static_container_image,
            depends_on=depends_on,
            for_each=for_each,
            providers=providers,
            skip_asset_creation_from_local_modules=skip_asset_creation_from_local_modules,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property
    @jsii.member(jsii_name="albArnOutput")
    def alb_arn_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "albArnOutput"))

    @builtins.property
    @jsii.member(jsii_name="albDnsNameOutput")
    def alb_dns_name_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "albDnsNameOutput"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc6bc87e77a4d6fd6fbcda084fb8977b27a258fc1f49c550e38e71354803447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="databasePassword")
    def database_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databasePassword"))

    @database_password.setter
    def database_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d425d79518da7226b008d8c3281fa0ca566aa42fc0e68f3e17cc336e6fc3ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databasePassword", value)

    @builtins.property
    @jsii.member(jsii_name="databaseUsername")
    def database_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseUsername"))

    @database_username.setter
    def database_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b3e47958bc36fd87959a4e9c26edab5ee3249d5a2c4f199ba7db66ad8d1777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseUsername", value)

    @builtins.property
    @jsii.member(jsii_name="datastoreS3BucketKmsKeyArn")
    def datastore_s3_bucket_kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datastoreS3BucketKmsKeyArn"))

    @datastore_s3_bucket_kms_key_arn.setter
    def datastore_s3_bucket_kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bfbd1a361cf4afb553e9d727acf368b68cda26c876dd4c9e055597cadcfebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datastoreS3BucketKmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="fargateExecutionRoleArn")
    def fargate_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fargateExecutionRoleArn"))

    @fargate_execution_role_arn.setter
    def fargate_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef2c68d9d83fb0f18c775e62c5399aa7d80226cfa7b28f02869c0745f627af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fargateExecutionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="metadataServiceSecurityGroupId")
    def metadata_service_security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataServiceSecurityGroupId"))

    @metadata_service_security_group_id.setter
    def metadata_service_security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef45de371baf94988c7a302c5c0791d37fabf61553fc38e6d5267d6c959e62af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataServiceSecurityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="metaflowDatastoreSysrootS3")
    def metaflow_datastore_sysroot_s3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowDatastoreSysrootS3"))

    @metaflow_datastore_sysroot_s3.setter
    def metaflow_datastore_sysroot_s3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec5fb7541a6f1ab02aa44ca8cd1ee016959e03f8fa96780e46093ec09fb1abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metaflowDatastoreSysrootS3", value)

    @builtins.property
    @jsii.member(jsii_name="metaflowVpcId")
    def metaflow_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metaflowVpcId"))

    @metaflow_vpc_id.setter
    def metaflow_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea8be11ee9e3fc2373d930e36a9659f82edcec1488baf005ae8d23abadbab38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metaflowVpcId", value)

    @builtins.property
    @jsii.member(jsii_name="rdsMasterInstanceEndpoint")
    def rds_master_instance_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rdsMasterInstanceEndpoint"))

    @rds_master_instance_endpoint.setter
    def rds_master_instance_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9154ca2360a1309414ea2cc0b5106b1a901ba2422ab695fec6bdbeeed8228cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rdsMasterInstanceEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePrefix")
    def resource_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePrefix"))

    @resource_prefix.setter
    def resource_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b08d385776578cd8694ad21e53429cb83cada7f3eb29718a3dfbb3190614a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSuffix")
    def resource_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSuffix"))

    @resource_suffix.setter
    def resource_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3842842760a106ff12c58a7950ed35c2fe5b136c45c47a0a79f04fed4d6d113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArn"))

    @s3_bucket_arn.setter
    def s3_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe392fccff5d75ed86c447ca64aad931d6d300ba1e99c9fb51c64617e6a431e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="standardTags")
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "standardTags"))

    @standard_tags.setter
    def standard_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a492867c7423b307c7d8e5e25e68991fe21ed171d068e12fbef01da008c505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardTags", value)

    @builtins.property
    @jsii.member(jsii_name="subnet1Id")
    def subnet1_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet1Id"))

    @subnet1_id.setter
    def subnet1_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b6a365f04205a245f3ef364145f42e029e2828ed451b494c4879670046439f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet1Id", value)

    @builtins.property
    @jsii.member(jsii_name="subnet2Id")
    def subnet2_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet2Id"))

    @subnet2_id.setter
    def subnet2_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556489ac6e306da5e59bc3d9ec953681d87eda6090ad523fc3ab43b359f9f20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet2Id", value)

    @builtins.property
    @jsii.member(jsii_name="albInternal")
    def alb_internal(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "albInternal"))

    @alb_internal.setter
    def alb_internal(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b8af5fbe854c3eaeaec1cee4c766b407942a30ef9f2015fdc86d672b1ffff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "albInternal", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdccb840899eb100fef835c0a9661b4183cb117e4b77d8152b0dc23eb7e58a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="extraUiBackendEnvVars")
    def extra_ui_backend_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraUiBackendEnvVars"))

    @extra_ui_backend_env_vars.setter
    def extra_ui_backend_env_vars(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49bfe430d77465bcb11288822cad0c697da5e3bbc0b08bc91dba0b649739c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraUiBackendEnvVars", value)

    @builtins.property
    @jsii.member(jsii_name="extraUiStaticEnvVars")
    def extra_ui_static_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extraUiStaticEnvVars"))

    @extra_ui_static_env_vars.setter
    def extra_ui_static_env_vars(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87b38ae7449ce9f327124f2a3dd8e85b76bc7a2dd2275bb4d82e8f6c8d77dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraUiStaticEnvVars", value)

    @builtins.property
    @jsii.member(jsii_name="iamPartition")
    def iam_partition(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamPartition"))

    @iam_partition.setter
    def iam_partition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cbcdc99c1cf886d3561acf14a99c58cc5fdd8e21f52e9b0f11c4c8d9399654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamPartition", value)

    @builtins.property
    @jsii.member(jsii_name="isGov")
    def is_gov(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isGov"))

    @is_gov.setter
    def is_gov(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652bef897e291f8923553a414ae53abd5365c8bdf16a1ecf59770045434210c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isGov", value)

    @builtins.property
    @jsii.member(jsii_name="uiAllowList")
    def ui_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "uiAllowList"))

    @ui_allow_list.setter
    def ui_allow_list(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e5cc613eacbfe5c0116ce4659f313295dfd1fe189d01e2f122e7f4254145ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiAllowList", value)

    @builtins.property
    @jsii.member(jsii_name="uiBackendContainerImage")
    def ui_backend_container_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiBackendContainerImage"))

    @ui_backend_container_image.setter
    def ui_backend_container_image(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3bfef78e216940ef62a862ace7f3c4d0609d8057b3604ca5fdb4878463495c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiBackendContainerImage", value)

    @builtins.property
    @jsii.member(jsii_name="uiStaticContainerImage")
    def ui_static_container_image(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiStaticContainerImage"))

    @ui_static_container_image.setter
    def ui_static_container_image(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa5d1b2d7f65af268ec5dd8469d09f4f06f7f81688c8eed458e2766148e894b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiStaticContainerImage", value)


@jsii.data_type(
    jsii_type="cdktf-metaflow-aws.MetaflowUiConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformModuleUserConfig],
    name_mapping={
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "providers": "providers",
        "skip_asset_creation_from_local_modules": "skipAssetCreationFromLocalModules",
        "certificate_arn": "certificateArn",
        "database_password": "databasePassword",
        "database_username": "databaseUsername",
        "datastore_s3_bucket_kms_key_arn": "datastoreS3BucketKmsKeyArn",
        "fargate_execution_role_arn": "fargateExecutionRoleArn",
        "metadata_service_security_group_id": "metadataServiceSecurityGroupId",
        "metaflow_datastore_sysroot_s3": "metaflowDatastoreSysrootS3",
        "metaflow_vpc_id": "metaflowVpcId",
        "rds_master_instance_endpoint": "rdsMasterInstanceEndpoint",
        "resource_prefix": "resourcePrefix",
        "resource_suffix": "resourceSuffix",
        "s3_bucket_arn": "s3BucketArn",
        "standard_tags": "standardTags",
        "subnet1_id": "subnet1Id",
        "subnet2_id": "subnet2Id",
        "alb_internal": "albInternal",
        "database_name": "databaseName",
        "extra_ui_backend_env_vars": "extraUiBackendEnvVars",
        "extra_ui_static_env_vars": "extraUiStaticEnvVars",
        "iam_partition": "iamPartition",
        "is_gov": "isGov",
        "ui_allow_list": "uiAllowList",
        "ui_backend_container_image": "uiBackendContainerImage",
        "ui_static_container_image": "uiStaticContainerImage",
    },
)
class MetaflowUiConfig(_cdktf_9a9027ec.TerraformModuleUserConfig):
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
        certificate_arn: builtins.str,
        database_password: builtins.str,
        database_username: builtins.str,
        datastore_s3_bucket_kms_key_arn: builtins.str,
        fargate_execution_role_arn: builtins.str,
        metadata_service_security_group_id: builtins.str,
        metaflow_datastore_sysroot_s3: builtins.str,
        metaflow_vpc_id: builtins.str,
        rds_master_instance_endpoint: builtins.str,
        resource_prefix: builtins.str,
        resource_suffix: builtins.str,
        s3_bucket_arn: builtins.str,
        standard_tags: typing.Mapping[builtins.str, builtins.str],
        subnet1_id: builtins.str,
        subnet2_id: builtins.str,
        alb_internal: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        iam_partition: typing.Optional[builtins.str] = None,
        is_gov: typing.Optional[builtins.bool] = None,
        ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_backend_container_image: typing.Optional[builtins.str] = None,
        ui_static_container_image: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param depends_on: 
        :param for_each: 
        :param providers: 
        :param skip_asset_creation_from_local_modules: 
        :param certificate_arn: SSL certificate ARN. The certificate will be used by the UI load balancer.
        :param database_password: The database password.
        :param database_username: The database username.
        :param datastore_s3_bucket_kms_key_arn: The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.
        :param fargate_execution_role_arn: This role allows Fargate to pull container images and logs. We'll use it as execution_role for our Fargate task
        :param metadata_service_security_group_id: The security group ID used by the MetaData service. This security group should allow connections to the RDS instance.
        :param metaflow_datastore_sysroot_s3: METAFLOW_DATASTORE_SYSROOT_S3 value.
        :param metaflow_vpc_id: VPC to deploy services into.
        :param rds_master_instance_endpoint: The database connection endpoint in address:port format.
        :param resource_prefix: Prefix given to all AWS resources to differentiate between applications.
        :param resource_suffix: Suffix given to all AWS resources to differentiate between environment and workspace.
        :param s3_bucket_arn: The ARN of the bucket used for Metaflow datastore.
        :param standard_tags: The standard tags to apply to every AWS resource. The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param subnet1_id: First private subnet used for availability zone redundancy.
        :param subnet2_id: Second private subnet used for availability zone redundancy.
        :param alb_internal: Defines whether the ALB is internal.
        :param database_name: The database name. Default: metaflow
        :param extra_ui_backend_env_vars: Additional environment variables for UI backend container. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param extra_ui_static_env_vars: Additional environment variables for UI static app. Default: [object Object] The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        :param iam_partition: IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is). Default: aws
        :param is_gov: Set to true if IAM partition is 'aws-us-gov'.
        :param ui_allow_list: A list of CIDRs the UI will be available to.
        :param ui_backend_container_image: Container image for UI backend.
        :param ui_static_container_image: Container image for the UI frontend app.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5276d8b80960b35c0faf6df84ae994caa00645be462af7902f52ea06c2d7fc73)
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument skip_asset_creation_from_local_modules", value=skip_asset_creation_from_local_modules, expected_type=type_hints["skip_asset_creation_from_local_modules"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument database_password", value=database_password, expected_type=type_hints["database_password"])
            check_type(argname="argument database_username", value=database_username, expected_type=type_hints["database_username"])
            check_type(argname="argument datastore_s3_bucket_kms_key_arn", value=datastore_s3_bucket_kms_key_arn, expected_type=type_hints["datastore_s3_bucket_kms_key_arn"])
            check_type(argname="argument fargate_execution_role_arn", value=fargate_execution_role_arn, expected_type=type_hints["fargate_execution_role_arn"])
            check_type(argname="argument metadata_service_security_group_id", value=metadata_service_security_group_id, expected_type=type_hints["metadata_service_security_group_id"])
            check_type(argname="argument metaflow_datastore_sysroot_s3", value=metaflow_datastore_sysroot_s3, expected_type=type_hints["metaflow_datastore_sysroot_s3"])
            check_type(argname="argument metaflow_vpc_id", value=metaflow_vpc_id, expected_type=type_hints["metaflow_vpc_id"])
            check_type(argname="argument rds_master_instance_endpoint", value=rds_master_instance_endpoint, expected_type=type_hints["rds_master_instance_endpoint"])
            check_type(argname="argument resource_prefix", value=resource_prefix, expected_type=type_hints["resource_prefix"])
            check_type(argname="argument resource_suffix", value=resource_suffix, expected_type=type_hints["resource_suffix"])
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument standard_tags", value=standard_tags, expected_type=type_hints["standard_tags"])
            check_type(argname="argument subnet1_id", value=subnet1_id, expected_type=type_hints["subnet1_id"])
            check_type(argname="argument subnet2_id", value=subnet2_id, expected_type=type_hints["subnet2_id"])
            check_type(argname="argument alb_internal", value=alb_internal, expected_type=type_hints["alb_internal"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument extra_ui_backend_env_vars", value=extra_ui_backend_env_vars, expected_type=type_hints["extra_ui_backend_env_vars"])
            check_type(argname="argument extra_ui_static_env_vars", value=extra_ui_static_env_vars, expected_type=type_hints["extra_ui_static_env_vars"])
            check_type(argname="argument iam_partition", value=iam_partition, expected_type=type_hints["iam_partition"])
            check_type(argname="argument is_gov", value=is_gov, expected_type=type_hints["is_gov"])
            check_type(argname="argument ui_allow_list", value=ui_allow_list, expected_type=type_hints["ui_allow_list"])
            check_type(argname="argument ui_backend_container_image", value=ui_backend_container_image, expected_type=type_hints["ui_backend_container_image"])
            check_type(argname="argument ui_static_container_image", value=ui_static_container_image, expected_type=type_hints["ui_static_container_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_arn": certificate_arn,
            "database_password": database_password,
            "database_username": database_username,
            "datastore_s3_bucket_kms_key_arn": datastore_s3_bucket_kms_key_arn,
            "fargate_execution_role_arn": fargate_execution_role_arn,
            "metadata_service_security_group_id": metadata_service_security_group_id,
            "metaflow_datastore_sysroot_s3": metaflow_datastore_sysroot_s3,
            "metaflow_vpc_id": metaflow_vpc_id,
            "rds_master_instance_endpoint": rds_master_instance_endpoint,
            "resource_prefix": resource_prefix,
            "resource_suffix": resource_suffix,
            "s3_bucket_arn": s3_bucket_arn,
            "standard_tags": standard_tags,
            "subnet1_id": subnet1_id,
            "subnet2_id": subnet2_id,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if providers is not None:
            self._values["providers"] = providers
        if skip_asset_creation_from_local_modules is not None:
            self._values["skip_asset_creation_from_local_modules"] = skip_asset_creation_from_local_modules
        if alb_internal is not None:
            self._values["alb_internal"] = alb_internal
        if database_name is not None:
            self._values["database_name"] = database_name
        if extra_ui_backend_env_vars is not None:
            self._values["extra_ui_backend_env_vars"] = extra_ui_backend_env_vars
        if extra_ui_static_env_vars is not None:
            self._values["extra_ui_static_env_vars"] = extra_ui_static_env_vars
        if iam_partition is not None:
            self._values["iam_partition"] = iam_partition
        if is_gov is not None:
            self._values["is_gov"] = is_gov
        if ui_allow_list is not None:
            self._values["ui_allow_list"] = ui_allow_list
        if ui_backend_container_image is not None:
            self._values["ui_backend_container_image"] = ui_backend_container_image
        if ui_static_container_image is not None:
            self._values["ui_static_container_image"] = ui_static_container_image

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def providers(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.TerraformProvider, _cdktf_9a9027ec.TerraformModuleProvider]]], result)

    @builtins.property
    def skip_asset_creation_from_local_modules(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("skip_asset_creation_from_local_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        '''SSL certificate ARN.

        The certificate will be used by the UI load balancer.
        '''
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_password(self) -> builtins.str:
        '''The database password.'''
        result = self._values.get("database_password")
        assert result is not None, "Required property 'database_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_username(self) -> builtins.str:
        '''The database username.'''
        result = self._values.get("database_username")
        assert result is not None, "Required property 'database_username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datastore_s3_bucket_kms_key_arn(self) -> builtins.str:
        '''The ARN of the KMS key used to encrypt the Metaflow datastore S3 bucket.'''
        result = self._values.get("datastore_s3_bucket_kms_key_arn")
        assert result is not None, "Required property 'datastore_s3_bucket_kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fargate_execution_role_arn(self) -> builtins.str:
        '''This role allows Fargate to pull container images and logs.

        We'll use it as execution_role for our Fargate task
        '''
        result = self._values.get("fargate_execution_role_arn")
        assert result is not None, "Required property 'fargate_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata_service_security_group_id(self) -> builtins.str:
        '''The security group ID used by the MetaData service.

        This security group should allow connections to the RDS instance.
        '''
        result = self._values.get("metadata_service_security_group_id")
        assert result is not None, "Required property 'metadata_service_security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metaflow_datastore_sysroot_s3(self) -> builtins.str:
        '''METAFLOW_DATASTORE_SYSROOT_S3 value.'''
        result = self._values.get("metaflow_datastore_sysroot_s3")
        assert result is not None, "Required property 'metaflow_datastore_sysroot_s3' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metaflow_vpc_id(self) -> builtins.str:
        '''VPC to deploy services into.'''
        result = self._values.get("metaflow_vpc_id")
        assert result is not None, "Required property 'metaflow_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_master_instance_endpoint(self) -> builtins.str:
        '''The database connection endpoint in address:port format.'''
        result = self._values.get("rds_master_instance_endpoint")
        assert result is not None, "Required property 'rds_master_instance_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_prefix(self) -> builtins.str:
        '''Prefix given to all AWS resources to differentiate between applications.'''
        result = self._values.get("resource_prefix")
        assert result is not None, "Required property 'resource_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_suffix(self) -> builtins.str:
        '''Suffix given to all AWS resources to differentiate between environment and workspace.'''
        result = self._values.get("resource_suffix")
        assert result is not None, "Required property 'resource_suffix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_arn(self) -> builtins.str:
        '''The ARN of the bucket used for Metaflow datastore.'''
        result = self._values.get("s3_bucket_arn")
        assert result is not None, "Required property 's3_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The standard tags to apply to every AWS resource.

        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("standard_tags")
        assert result is not None, "Required property 'standard_tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def subnet1_id(self) -> builtins.str:
        '''First private subnet used for availability zone redundancy.'''
        result = self._values.get("subnet1_id")
        assert result is not None, "Required property 'subnet1_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet2_id(self) -> builtins.str:
        '''Second private subnet used for availability zone redundancy.'''
        result = self._values.get("subnet2_id")
        assert result is not None, "Required property 'subnet2_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alb_internal(self) -> typing.Optional[builtins.bool]:
        '''Defines whether the ALB is internal.'''
        result = self._values.get("alb_internal")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The database name.

        :default: metaflow
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_ui_backend_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables for UI backend container.

        :default:

        [object Object]
        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("extra_ui_backend_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def extra_ui_static_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional environment variables for UI static app.

        :default:

        [object Object]
        The property type contains a map, they have special handling, please see {@link cdk.tf/module-map-inputs the docs}
        '''
        result = self._values.get("extra_ui_static_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def iam_partition(self) -> typing.Optional[builtins.str]:
        '''IAM Partition (Select aws-us-gov for AWS GovCloud, otherwise leave as is).

        :default: aws
        '''
        result = self._values.get("iam_partition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_gov(self) -> typing.Optional[builtins.bool]:
        '''Set to true if IAM partition is 'aws-us-gov'.'''
        result = self._values.get("is_gov")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ui_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CIDRs the UI will be available to.'''
        result = self._values.get("ui_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ui_backend_container_image(self) -> typing.Optional[builtins.str]:
        '''Container image for UI backend.'''
        result = self._values.get("ui_backend_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ui_static_container_image(self) -> typing.Optional[builtins.str]:
        '''Container image for the UI frontend app.'''
        result = self._values.get("ui_static_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowUiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Metaflow",
    "MetaflowCommon",
    "MetaflowCommonConfig",
    "MetaflowComputation",
    "MetaflowComputationConfig",
    "MetaflowConfig",
    "MetaflowDatastore",
    "MetaflowDatastoreConfig",
    "MetaflowMetadataService",
    "MetaflowMetadataServiceConfig",
    "MetaflowStepFunctions",
    "MetaflowStepFunctionsConfig",
    "MetaflowUi",
    "MetaflowUiConfig",
]

publication.publish()

def _typecheckingstub__93c06ad4407f13baa7e439389be7009cb53f5917bf8bb8301d53e60841d5a2f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enable_step_functions: builtins.bool,
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    vpc_cidr_blocks: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    with_public_ip: builtins.bool,
    access_list_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_type: typing.Optional[builtins.str] = None,
    compute_environment_desired_vcpus: typing.Optional[jsii.Number] = None,
    compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_max_vcpus: typing.Optional[jsii.Number] = None,
    compute_environment_min_vcpus: typing.Optional[jsii.Number] = None,
    enable_custom_batch_container_registry: typing.Optional[builtins.bool] = None,
    extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    launch_template_http_endpoint: typing.Optional[builtins.str] = None,
    launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    launch_template_http_tokens: typing.Optional[builtins.str] = None,
    metadata_service_container_image: typing.Optional[builtins.str] = None,
    metadata_service_enable_api_basic_auth: typing.Optional[builtins.bool] = None,
    metadata_service_enable_api_gateway: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Any = None,
    resource_suffix: typing.Any = None,
    ui_alb_internal: typing.Optional[builtins.bool] = None,
    ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_certificate_arn: typing.Optional[builtins.str] = None,
    ui_static_container_image: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb50281ad55eb00ca03f6762a1443bbe78e5bd31c4d27900d6e0ae9f9bf7fef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff6d39379d3599872dc31929f887c1be67862648326f34149282ad1aca244d2(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3104ef85cbfa0eecdce98973443469d7624e1f6aa06060ebad38456d2dabef(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c532d1cc3c745c3b2ccec31aead3b3e91fdf75cb56295823cf9906777e726152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea21d93f5e88f978a16a43144209f48445922f020105aacd3abe5cc6cadf1b5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478e049146dcb4ee8a5f4531a5a7f14d0758cee6344aa2052083d1c08d4ad097(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c9778cb6c92698b4f839d39ebbca09d0a8f022826361ae20e3b83a6ef64265(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49d45ffe17715cb7ae4531b41849c25fa850f0b5b431fd2d6bb6e661669fd78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee4c67d85d6e5fc036d39d3f361b783407c8a5f8d50618dfae32a5225a03c8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1973e042217de6e6f5b280091fdf9b3dcbd2de2cabc7bafb7361b01ed197ed46(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676a229b069adc690f1052b9d6f132c397e0e62954f1a452c261b6302a582105(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf24682646d2876fcf96698ebcea5d6d0f10cea43df8ce73deb31c35e45dc3ac(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d6e2f71358314e2f37ba23d9b7d4e607e75607c2bfbd0fb6dcc40ed9672e4c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d59d5cc8a6a683dcf1987cb086023905a765427846e5ba3390474360d01dafb(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772c2bc41942fda9cc20de5b9b6848c89a651cc8b42b7f5ae478f75fd6fd0892(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a414061d9859747dcb427c2a19f6f22a1fe080cabe5cca6eaebdac35a485be(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd147f412a8b39ef0f8167b70b73c49681a6edf04a7a32e41fee08cba7b06b8(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e756c9d0c1c70d93e99b5d430fefc9d06031fd596e7e0ddec8670e708dcef27(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a3b53a82e6405da1718e3029d7c188d7406563024ec0f40d3f1042279d203a(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d2795d7bc6f9added7e3e24214eaf15d16547f6d985637334d44d5c49e6d5d(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f127554094db4bdc6921aee6184aa9381392bb785787ecb8de3b9fc338936be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6c9c5b35ac8306bdba4892798aaf6174403d9ca5bfef9f2b18e5c0ebf0dd49(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f64c48c0a92a0a558b47778f4c4beccb8db9986204bfe31e478d7871060b7f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0704370647cc87d9018fee61de4b4849ea6771c17ea86b16bb294a8ac39ce8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4c7bcbb581d4d67565bf77b7a9e59779b23a7516252f8fd4a1e6b95a075273(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b822d8fb37c4a8eae79447e95fe73ff9b4ed6f363429e3ac40a44afaec25139(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e8990133329003472e3bd91c40a28505c11fb7a6c1c52ec1a99f0dc411969f(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6690c3a0558f331145d42546286abb0b85614a3846c1003d89dce0c8ee3038b1(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7601bed4137cb8da1d8ac6b8140a5de45a85a74b19c6cefd4fc224107a248205(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55984efcfa102463add4923b3a85fedd463f4cf50db266b4751651a04ebfea92(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aad21182d95ab0878c87830af84225091693ac73034c5f263fa98da022653de(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829841cfa9884aede1cde2a81e6bcce493a0fd5a84870ef5e8bcdc0283c09260(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edee3089650317e6ec3c36b0314673fc212dd01f36da7c96d6d898dae56b3f1f(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f983a1998df315902d0c7e7a0fb25570052d3a26ce5698308015b3a7a9130f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_environment_desired_vcpus: jsii.Number,
    compute_environment_instance_types: typing.Sequence[builtins.str],
    compute_environment_max_vcpus: jsii.Number,
    compute_environment_min_vcpus: jsii.Number,
    metaflow_vpc_id: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    batch_type: typing.Optional[builtins.str] = None,
    compute_environment_additional_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_allocation_strategy: typing.Optional[builtins.str] = None,
    compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    launch_template_http_endpoint: typing.Optional[builtins.str] = None,
    launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    launch_template_http_tokens: typing.Optional[builtins.str] = None,
    launch_template_image_id: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57062ffa92f7a58dae40a2f134889f76d10a4d19ad4d86ebe3efb4ae2a8e862(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065cf6c52a834ffeb56e26fc492d7d2935035e47b2a22a76efccad70c78d2754(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb48b24e6bcdf5a72b558b27c51854727d4a3ec24670e1468b1b136461b44560(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b14b11ee0d68aa742018b8420ab5add53e1c6183be316c6b55124d8b42324f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ca91f38605dea860f051abd00d4e5708502f1fb83478c66fc7138fe053d9db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40ed427e87e9845d794e667a41fd3c52ae37800e624ac5488a244ec78d3e89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4289b858cf5365a8fb0cb6280562bc9f10cab5fd946fc35d018f086e717f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd2126d7b5a6921fef7c8df8f2828d1b2f9a940904716fe61377ab4cff23057(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f30d7dc31f769468477fea012169b6ce85386dc14f7fce5bd340f8b4b28374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c09b9e6d383ac82f1d57b61a3f2d88612c28a1c6ab924943d68ca3f25e3842c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b921e269682b398442728d204bea0c6a9ef787a6e46f73eaae3dbc31d08df3c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d70ebcf652e1c3b24eb9176b48f008246eb08aad88a5a4f12a7232e8b6d7d7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8699cf5f5266ee4d09382d9b5e6d181b5603ec7fb6fd40313c37c3438f219c07(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733bb522b4e82e24a327e4dc7f5d0aed5411073c5c71ceb236c718caa55c76e4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ff2b459476b5cd6ddeacff3f7587bef82e57db83823eb9c0c1d5482e0c8022(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324d8ba07b9a09e4c6d7ef4d778a2e709fe6c5d1e19b351f00ab888a46be65b0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabefb551e91ad354831b3fc9fdd98337e5eaf41b7492986f8db3bd2818e4592(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bbf4a716fef7912c35298ca15a5e0ddb82769210bd4ebc2ad62ed507d465a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc139296daecd54b333e6ba3131e62f86553b1d3806d95babb61f3d2d77caba(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401da8cd2fddb490d1fa268ca9e57db9a6120e4cc94e907002f2df769fbdba53(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    compute_environment_desired_vcpus: jsii.Number,
    compute_environment_instance_types: typing.Sequence[builtins.str],
    compute_environment_max_vcpus: jsii.Number,
    compute_environment_min_vcpus: jsii.Number,
    metaflow_vpc_id: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    batch_type: typing.Optional[builtins.str] = None,
    compute_environment_additional_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_allocation_strategy: typing.Optional[builtins.str] = None,
    compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    launch_template_http_endpoint: typing.Optional[builtins.str] = None,
    launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    launch_template_http_tokens: typing.Optional[builtins.str] = None,
    launch_template_image_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b011ea088374cb11d8943508b28b9104cfae57e1e826f167597e09fca21f6cc(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    enable_step_functions: builtins.bool,
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    vpc_cidr_blocks: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    with_public_ip: builtins.bool,
    access_list_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    batch_type: typing.Optional[builtins.str] = None,
    compute_environment_desired_vcpus: typing.Optional[jsii.Number] = None,
    compute_environment_egress_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    compute_environment_max_vcpus: typing.Optional[jsii.Number] = None,
    compute_environment_min_vcpus: typing.Optional[jsii.Number] = None,
    enable_custom_batch_container_registry: typing.Optional[builtins.bool] = None,
    extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    launch_template_http_endpoint: typing.Optional[builtins.str] = None,
    launch_template_http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    launch_template_http_tokens: typing.Optional[builtins.str] = None,
    metadata_service_container_image: typing.Optional[builtins.str] = None,
    metadata_service_enable_api_basic_auth: typing.Optional[builtins.bool] = None,
    metadata_service_enable_api_gateway: typing.Optional[builtins.bool] = None,
    resource_prefix: typing.Any = None,
    resource_suffix: typing.Any = None,
    ui_alb_internal: typing.Optional[builtins.bool] = None,
    ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_certificate_arn: typing.Optional[builtins.str] = None,
    ui_static_container_image: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6211efd6f48fadd33fe149c71d77f56745e949d7c1ecc68d62e84e4e5d215e5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    metadata_service_security_group_id: builtins.str,
    metaflow_vpc_id: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    db_engine: typing.Optional[builtins.str] = None,
    db_engine_version: typing.Optional[builtins.str] = None,
    db_instance_type: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    db_username: typing.Optional[builtins.str] = None,
    force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ad2e4372074cd8fbdf74746941e608370389038e220cf960efd2cd82afceb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d5d4490bef28bf5250debe48e1b318ce0c0ea372801288a7e65a8da0319989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510cc062fc31c1397a4fa1196e5209c58ad5f2ad7dab8d7ec09f302d15ffb795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b23e041919ee471ed3ab82c932ee018458cb307209604da9819feed6266087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e71912e31dfc49dedf411886c3ced0707524e8c1346c8eddc4a2199a74ad5a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb5467e0db60879b57c05ddb1ba73c99e588b90ec6267ed7351841561298da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e5d713366e5074a307bf00f159e0f7f93939b5fc4cc2e2f3d17a091a299507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c48c8ec5aa5bae49ba4b74b630e87ca797173c8d904f2105c0f4d098686993(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c1cef82f0bb29d3978522e75f6bc9a6ed488ddcb38d2427cebf9b14b773d59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e043cbc9aa4b915e2e06af4fb9a28cb48a8fa8b9674f450c7c8653022474197(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a58f7fdf31431db9e44fc3d1539eb341fe02ca965590c8a0c791ed3b1607ee4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b30e9057d5a3b05c91390d9843aaa08d298e7e1583af48b661bb9ec79b2964(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e9ecdfbd4ed97e253ba9bdb13379c80a40d61b1ca453aac0c25d9fb264c9de(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c4234a39f77d9aef76201cffcf80f6f8750d1b26600201ff54d15fbe36c3f8(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    metadata_service_security_group_id: builtins.str,
    metaflow_vpc_id: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    db_engine: typing.Optional[builtins.str] = None,
    db_engine_version: typing.Optional[builtins.str] = None,
    db_instance_type: typing.Optional[builtins.str] = None,
    db_name: typing.Optional[builtins.str] = None,
    db_username: typing.Optional[builtins.str] = None,
    force_destroy_s3_bucket: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a5684d135286dde8f18f1429942040c15944ae4768fe62e56efc200a74f200(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_list_cidr_blocks: typing.Sequence[builtins.str],
    database_password: builtins.str,
    database_username: builtins.str,
    datastore_s3_bucket_kms_key_arn: builtins.str,
    fargate_execution_role_arn: builtins.str,
    metaflow_vpc_id: builtins.str,
    rds_master_instance_endpoint: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    vpc_cidr_blocks: typing.Sequence[builtins.str],
    with_public_ip: builtins.bool,
    database_name: typing.Optional[builtins.str] = None,
    enable_api_basic_auth: typing.Optional[builtins.bool] = None,
    enable_api_gateway: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    is_gov: typing.Optional[builtins.bool] = None,
    metadata_service_container_image: typing.Optional[builtins.str] = None,
    metadata_service_cpu: typing.Optional[jsii.Number] = None,
    metadata_service_memory: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177ba7546a8a3c8052b7177f00dc008db8de159be8527166073bab19b3401c57(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0e4fe919decd061264a28cb3357c372b21d6d7b82cf9b92ff53e162af49534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474b52ff7f03d32e140a0664ddf608ae1c30cb557558f89eec7a1b01744b9952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7138b0f8867684ff60462fca6129b805183bf3f2aa2dd40377a2daa0857f99c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e8604fe768f188c267aa732f99bd8ee8e4a3ae9910e0d828bf989a29a86e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7984f06df03fc9c5263efd600d0a6c9121d80467da55fb020230a351cfc170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9c829b7203dce2629a0248654455e3212476465f04b8b820f77ca00eac78a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604aa7780d3092325295cdbdbfac5ad5051dd6415ed6ad613bc9ec20cdd018f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bce855b9373ae829f83a95498f9f228e400614fd6f866823ec24a123ee17cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9df2c5fcd68ca6a8ce730ec192777f253900cc95abdbea3c83b7ddfc3513a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c120ad64f66a5b4271f1a34a292ff49dca70e405f53f621bd3d7a08511d6732b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff5de91741a05a222c5d31809a2970561c1727003febfac6040d466f24852c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafb6d9f85e432e4ba67c33d85dc77267445c3df672a5d312cebaa7ed1519fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0680e3170408a6718d3b6e34bafb9c1fa0f581619badc079f4326a286d6e6c01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1228cba52ba2f1a47f0a02dbfc3a16e562b13a237640721aad2bb8bd6f01e53e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a18b3d3dff6a35a21ec14ce7e0f2de207879ca380d1c6f4ff266b60c571ed21(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcafdac999ad6971d5956edc302564c5d9fab945a2284c866c1d2318aa30889d(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9945e95e0b67e0de746c3f554642536ed64bcd47c96c2592a848013bef6483(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a8b90ad5580e42b9b600cd8ee832cc9f8776edb5e0ebbd1e66770484e2d479(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c571d34d2187c67c2e813249c279cbb433561eeaeaaae9f10f56afeb894774f5(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc9ee5e9f85cc93de30ec3f703572f339ab432c0b382e28f844b4b672c7b688(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a611b11fa101496188393844d016894c5d503f47cca6b53ae12d0b0514987f8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fca6d4146676b2adec57f9a725d309cd1b48d7adaeffefead221b13f366abb8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d87e5f7076de12631af86993934ec6cb65adc08c125543b3bc9e7b29929dacc(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    access_list_cidr_blocks: typing.Sequence[builtins.str],
    database_password: builtins.str,
    database_username: builtins.str,
    datastore_s3_bucket_kms_key_arn: builtins.str,
    fargate_execution_role_arn: builtins.str,
    metaflow_vpc_id: builtins.str,
    rds_master_instance_endpoint: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    vpc_cidr_blocks: typing.Sequence[builtins.str],
    with_public_ip: builtins.bool,
    database_name: typing.Optional[builtins.str] = None,
    enable_api_basic_auth: typing.Optional[builtins.bool] = None,
    enable_api_gateway: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    is_gov: typing.Optional[builtins.bool] = None,
    metadata_service_container_image: typing.Optional[builtins.str] = None,
    metadata_service_cpu: typing.Optional[jsii.Number] = None,
    metadata_service_memory: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0bf7a24bd4485357457ded48e181f9e0173a7df7f7e9b463cebdcd02479cce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    batch_job_queue_arn: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    s3_bucket_kms_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    active: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25fddf5fdf481b8466eeae5fb5d73962a617af6d875a6d10c394b97ab58ce24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9242d50a36034e44266cace376bbb4745c9d650b53664806909fe159dba00b61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c1c020ac6f73d1ed5076f4473957720420af4e3e012eea0a71f5e1f8712bde2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae71cf2850b010ef03283211ddc1a08e6aa6b560024d95f5a6ccb38e9e3b1441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e86669da1bd161caf6c2e64713d818918439c6850e47f7e29a3701e14b98ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ebefe46f560ea7cf518e20d243517210896e8588c5fab179c5872c863613ea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7effed9e5832f1c1eb68d176d4787369c06bf7492507837babc71c9283710bdf(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa186e83bdba71785915a8de994799016a90dba2e6f394d511e2d986ad88e06(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2a2ba9ab32f59f0ffc89f0f30266bfc363285642496442ad7559da77da2e16(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    batch_job_queue_arn: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    s3_bucket_kms_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    active: typing.Optional[builtins.bool] = None,
    iam_partition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de8555760d621a1ce7c7248af48f7343ef0a843ed23f412c163d01dcdadf88e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate_arn: builtins.str,
    database_password: builtins.str,
    database_username: builtins.str,
    datastore_s3_bucket_kms_key_arn: builtins.str,
    fargate_execution_role_arn: builtins.str,
    metadata_service_security_group_id: builtins.str,
    metaflow_datastore_sysroot_s3: builtins.str,
    metaflow_vpc_id: builtins.str,
    rds_master_instance_endpoint: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    alb_internal: typing.Optional[builtins.bool] = None,
    database_name: typing.Optional[builtins.str] = None,
    extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    is_gov: typing.Optional[builtins.bool] = None,
    ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_backend_container_image: typing.Optional[builtins.str] = None,
    ui_static_container_image: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc6bc87e77a4d6fd6fbcda084fb8977b27a258fc1f49c550e38e71354803447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d425d79518da7226b008d8c3281fa0ca566aa42fc0e68f3e17cc336e6fc3ea3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b3e47958bc36fd87959a4e9c26edab5ee3249d5a2c4f199ba7db66ad8d1777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bfbd1a361cf4afb553e9d727acf368b68cda26c876dd4c9e055597cadcfebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef2c68d9d83fb0f18c775e62c5399aa7d80226cfa7b28f02869c0745f627af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef45de371baf94988c7a302c5c0791d37fabf61553fc38e6d5267d6c959e62af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec5fb7541a6f1ab02aa44ca8cd1ee016959e03f8fa96780e46093ec09fb1abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea8be11ee9e3fc2373d930e36a9659f82edcec1488baf005ae8d23abadbab38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9154ca2360a1309414ea2cc0b5106b1a901ba2422ab695fec6bdbeeed8228cef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b08d385776578cd8694ad21e53429cb83cada7f3eb29718a3dfbb3190614a82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3842842760a106ff12c58a7950ed35c2fe5b136c45c47a0a79f04fed4d6d113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe392fccff5d75ed86c447ca64aad931d6d300ba1e99c9fb51c64617e6a431e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a492867c7423b307c7d8e5e25e68991fe21ed171d068e12fbef01da008c505(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b6a365f04205a245f3ef364145f42e029e2828ed451b494c4879670046439f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556489ac6e306da5e59bc3d9ec953681d87eda6090ad523fc3ab43b359f9f20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b8af5fbe854c3eaeaec1cee4c766b407942a30ef9f2015fdc86d672b1ffff6(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdccb840899eb100fef835c0a9661b4183cb117e4b77d8152b0dc23eb7e58a85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49bfe430d77465bcb11288822cad0c697da5e3bbc0b08bc91dba0b649739c37(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87b38ae7449ce9f327124f2a3dd8e85b76bc7a2dd2275bb4d82e8f6c8d77dbf(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cbcdc99c1cf886d3561acf14a99c58cc5fdd8e21f52e9b0f11c4c8d9399654(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652bef897e291f8923553a414ae53abd5365c8bdf16a1ecf59770045434210c0(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e5cc613eacbfe5c0116ce4659f313295dfd1fe189d01e2f122e7f4254145ae(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3bfef78e216940ef62a862ace7f3c4d0609d8057b3604ca5fdb4878463495c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa5d1b2d7f65af268ec5dd8469d09f4f06f7f81688c8eed458e2766148e894b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5276d8b80960b35c0faf6df84ae994caa00645be462af7902f52ea06c2d7fc73(
    *,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    providers: typing.Optional[typing.Sequence[typing.Union[_cdktf_9a9027ec.TerraformProvider, typing.Union[_cdktf_9a9027ec.TerraformModuleProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_asset_creation_from_local_modules: typing.Optional[builtins.bool] = None,
    certificate_arn: builtins.str,
    database_password: builtins.str,
    database_username: builtins.str,
    datastore_s3_bucket_kms_key_arn: builtins.str,
    fargate_execution_role_arn: builtins.str,
    metadata_service_security_group_id: builtins.str,
    metaflow_datastore_sysroot_s3: builtins.str,
    metaflow_vpc_id: builtins.str,
    rds_master_instance_endpoint: builtins.str,
    resource_prefix: builtins.str,
    resource_suffix: builtins.str,
    s3_bucket_arn: builtins.str,
    standard_tags: typing.Mapping[builtins.str, builtins.str],
    subnet1_id: builtins.str,
    subnet2_id: builtins.str,
    alb_internal: typing.Optional[builtins.bool] = None,
    database_name: typing.Optional[builtins.str] = None,
    extra_ui_backend_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    extra_ui_static_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    iam_partition: typing.Optional[builtins.str] = None,
    is_gov: typing.Optional[builtins.bool] = None,
    ui_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_backend_container_image: typing.Optional[builtins.str] = None,
    ui_static_container_image: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
