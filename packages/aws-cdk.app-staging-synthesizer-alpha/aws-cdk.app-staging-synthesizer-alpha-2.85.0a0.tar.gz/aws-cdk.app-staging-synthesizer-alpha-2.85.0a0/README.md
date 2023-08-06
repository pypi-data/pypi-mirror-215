# App Staging Synthesizer

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library includes constructs aimed at replacing the current model of bootstrapping and providing
greater control of the bootstrap experience to the CDK user. The important constructs in this library
are as follows:

* the `IStagingResources` interface: a framework for an app-level bootstrap stack that handles
  file assets and docker assets.
* the `DefaultStagingStack`, which is a works-out-of-the-box implementation of the `IStagingResources`
  interface.
* the `AppStagingSynthesizer`, a new CDK synthesizer that will synthesize CDK applications with
  the staging resources provided.

> As this library is `experimental`, there are features that are not yet implemented. Please look
> at the list of [Known Limitations](#known-limitations) before getting started.

To get started, update your CDK App with a new `defaultStackSynthesizer`:

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id"
    )
)
```

This will introduce a `DefaultStagingStack` in your CDK App and staging assets of your App
will live in the resources from that stack rather than the CDK Bootstrap stack.

If you are migrating from a different version of synthesis your updated CDK App will target
the resources in the `DefaultStagingStack` and no longer be tied to the bootstrapped resources
in your account.

## Bootstrap Model

Our current bootstrap model looks like this, when you run `cdk bootstrap aws://<account>/<region>` :

```text
┌───────────────────────────────────┐┌────────────────────────┐┌────────────────────────┐
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│          ┌───────────────┐        ││    ┌──────────────┐    ││    ┌──────────────┐    │
│          │Bootstrap Stack│        ││    │  CDK App 1   │    ││    │  CDK App 2   │    │
│          └───────────────┘        ││    └──────────────┘    ││    └──────────────┘    │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│   ┌───────────────────────────┐   ││     ┌────────────┐     ││                        │
│   │IAM Role for CFN execution │   ││┌────│  S3 Asset  │     ││                        │
│   │    IAM Role for lookup    │   │││    └────────────┘     ││                        │
│   │  IAM Role for deployment  │   │││                       ││                        │
│   └───────────────────────────┘   │││                       ││     ┌─────────────┐    │
│                                   │││            ┌──────────┼┼─────│  S3 Asset   │    │
│                                   │││            │          ││     └─────────────┘    │
│ ┌───────────────────────────────┐ │││            │          ││                        │
│ │ IAM Role for File Publishing  │ │││            │          ││                        │
│ │ IAM Role for Image Publishing │ │││            │          ││                        │
│ └───────────────────────────────┘ │││            │          ││                        │
│                                   │││            │          ││                        │
│  ┌─────────────────────────────┐  │││            │          ││                        │
│  │S3 Bucket for Staging Assets │  │││            │          ││                        │
│  │     KMS Key encryption      │◀─┼┼┴────────────┘          ││      ┌────────────┐    │
│  └─────────────────────────────┘  ││             ┌──────────┼┼───── │ ECR Asset  │    │
│                                   ││             │          ││      └────────────┘    │
│                                   ││             │          ││                        │
│┌─────────────────────────────────┐││             │          ││                        │
││ECR Repository for Staging Assets◀┼┼─────────────┘          ││                        │
│└─────────────────────────────────┘││                        ││                        │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
│                                   ││                        ││                        │
└───────────────────────────────────┘└────────────────────────┘└────────────────────────┘
```

Your CDK Application utilizes these resources when deploying. For example, if you have a file asset,
it gets uploaded to the S3 Staging Bucket using the File Publishing Role when you run `cdk deploy`.

This library introduces an alternate model to bootstrapping, by splitting out essential CloudFormation IAM roles
and staging resources. There will still be a Bootstrap Stack, but this will only contain IAM roles necessary for
CloudFormation deployment. Each CDK App will instead be in charge of its own staging resources, including the
S3 Bucket, ECR Repositories, and associated IAM roles. It works like this:

The Staging Stack will contain, on a per-need basis,

* 1 S3 Bucket with KMS encryption for all file assets in the CDK App.
* An ECR Repository *per* image (and its revisions).
* IAM roles with access to the Bucket and Repositories.

```text
┌─────────────────────────────┐┌───────────────────────────────────────┐┌───────────────────────────────────────┐
│                             ││                                       ││                                       │
│      ┌───────────────┐      ││             ┌──────────────┐          ││             ┌──────────────┐          │
│      │Bootstrap Stack│      ││             │  CDK App 1   │          ││             │  CDK App 2   │          │
│      └───────────────┘      ││             └──────────────┘          ││             └──────────────┘          │
│                             ││┌──────────────────┐                   ││┌──────────────────┐                   │
│                             │││ ┌──────────────┐ │                   │││ ┌──────────────┐ │                   │
│                             │││ │Staging Stack │ │                   │││ │Staging Stack │ │                   │
│                             │││ └──────────────┘ │                   │││ └──────────────┘ │                   │
│                             │││                  │                   │││                  │                   │
│                             │││                  │                   │││                  │                   │
│                             │││┌────────────────┐│     ┌────────────┐│││┌────────────────┐│     ┌────────────┐│
│                             ││││  IAM Role for  ││ ┌───│  S3 Asset  │││││  IAM Role for  ││ ┌───│  S3 Asset  ││
│                             ││││File Publishing ││ │   └────────────┘││││File Publishing ││ │   └────────────┘│
│                             │││└────────────────┘│ │                 ││││  IAM Role for  ││ │                 │
│                             │││                  │ │                 ││││Image Publishing││ │                 │
│┌───────────────────────────┐│││                  │ │                 │││└────────────────┘│ │                 │
││IAM Role for CFN execution ││││                  │ │                 │││                  │ │                 │
││    IAM Role for lookup    ││││                  │ │                 │││                  │ │                 │
││  IAM Role for deployment  ││││┌────────────────┐│ │                 │││┌────────────────┐│ │                 │
│└───────────────────────────┘││││ S3 Bucket for  ││ │                 ││││ S3 Bucket for  ││ │                 │
│                             ││││ Staging Assets │◀─┘                 ││││ Staging Assets │◀─┘                 │
│                             │││└────────────────┘│                   │││└────────────────┘│      ┌───────────┐│
│                             │││                  │                   │││                  │  ┌───│ ECR Asset ││
│                             │││                  │                   │││┌────────────────┐│  │   └───────────┘│
│                             │││                  │                   ││││ ECR Repository ││  │                │
│                             │││                  │                   ││││  for Staging   │◀──┘                │
│                             │││                  │                   ││││     Assets     ││                   │
│                             │││                  │                   │││└────────────────┘│                   │
│                             │││                  │                   │││                  │                   │
│                             │││                  │                   │││                  │                   │
│                             │││                  │                   │││                  │                   │
│                             │││                  │                   │││                  │                   │
│                             │││                  │                   │││                  │                   │
│                             ││└──────────────────┘                   ││└──────────────────┘                   │
└─────────────────────────────┘└───────────────────────────────────────┘└───────────────────────────────────────┘
```

This allows staging resources to be created when needed next to the CDK App. It has the following
benefits:

* Resources between separate CDK Apps are separated so they can be cleaned up and lifecycle
  controlled individually.
* Users have a familiar way to customize staging resources in the CDK Application.

## Using the Default Staging Stack per Environment

The most common use case will be to use the built-in default resources. In this scenario, the
synthesizer will create a new Staging Stack in each environment the CDK App is deployed to store
its staging resources. To use this kind of synthesizer, use `AppStagingSynthesizer.defaultResources()`.

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id"
    )
)
```

Every CDK App that uses the `DefaultStagingStack` must include an `appId`. This should
be an identifier unique to the app and is used to differentiate staging resources associated
with the app.

### Default Staging Stack

The Default Staging Stack includes all the staging resources necessary for CDK Assets. The below example
is of a CDK App using the `AppStagingSynthesizer` and creating a file asset for the Lambda Function
source code. As part of the `DefaultStagingStack`, an S3 bucket and IAM role will be created that will be
used to upload the asset to S3.

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(app_id="my-app-id")
)

stack = Stack(app, "my-stack")

lambda_.Function(stack, "lambda",
    code=lambda_.AssetCode.from_asset(path.join(__dirname, "assets")),
    handler="index.handler",
    runtime=lambda_.Runtime.PYTHON_3_9
)

app.synth()
```

### Custom Roles

You can customize some or all of the roles you'd like to use in the synthesizer as well,
if all you need is to supply custom roles (and not change anything else in the `DefaultStagingStack`):

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id",
        deployment_identities=DeploymentIdentities.specify_roles(
            cloud_formation_execution_role=BootstrapRole.from_role_arn("arn:aws:iam::123456789012:role/Execute"),
            deployment_role=BootstrapRole.from_role_arn("arn:aws:iam::123456789012:role/Deploy"),
            lookup_role=BootstrapRole.from_role_arn("arn:aws:iam::123456789012:role/Lookup")
        )
    )
)
```

Or, you can ask to use the CLI credentials that exist at deploy-time.
These credentials must have the ability to perform CloudFormation calls,
lookup resources in your account, and perform CloudFormation deployment.
For a full list of what is necessary, see `LookupRole`, `DeploymentActionRole`,
and `CloudFormationExecutionRole` in the
[bootstrap template](https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk/lib/api/bootstrap/bootstrap-template.yaml).

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id",
        deployment_identities=DeploymentIdentities.cli_credentials()
    )
)
```

The default staging stack will create roles to publish to the S3 bucket and ECR repositories,
assumable by the deployment role. You can also specify an existing IAM role for the
`fileAssetPublishingRole` or `imageAssetPublishingRole`:

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id",
        file_asset_publishing_role=BootstrapRole.from_role_arn("arn:aws:iam::123456789012:role/S3Access"),
        image_asset_publishing_role=BootstrapRole.from_role_arn("arn:aws:iam::123456789012:role/ECRAccess")
    )
)
```

### Deploy Time S3 Assets

There are two types of assets:

* Assets used only during deployment. These are used to hand off a large piece of data to another
  service, that will make a private copy of that data. After deployment, the asset is only necessary for
  a potential future rollback.
* Assets accessed throughout the running life time of the application.

Examples of assets that are only used at deploy time are CloudFormation Templates and Lambda Code
bundles. Examples of assets accessed throughout the life time of the application are script files
downloaded to run in a CodeBuild Project, or on EC2 instance startup. ECR images are always application
life-time assets. S3 deploy time assets are stored with a `deploy-time/` prefix, and a lifecycle rule will collect them after a configurable number of days.

Lambda assets are by default marked as deploy time assets:

```python
# stack: Stack

lambda_.Function(stack, "lambda",
    code=lambda_.AssetCode.from_asset(path.join(__dirname, "assets")),  # lambda marks deployTime = true
    handler="index.handler",
    runtime=lambda_.Runtime.PYTHON_3_9
)
```

Or, if you want to create your own deploy time asset:

```python
from aws_cdk.aws_s3_assets import Asset

# stack: Stack

asset = Asset(stack, "deploy-time-asset",
    deploy_time=True,
    path=path.join(__dirname, "./deploy-time-asset")
)
```

By default, we store deploy time assets for 30 days, but you can change this number by specifying
`deployTimeFileAssetLifetime`. The number you specify here is how long you will be able to roll back
to a previous version of an application just by doing a CloudFormation deployment with the old
template, without rebuilding and republishing assets.

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id",
        deploy_time_file_asset_lifetime=Duration.days(100)
    )
)
```

### Lifecycle Rules on ECR Repositories

By default, we store a maximum of 3 revisions of a particular docker image asset. This allows
for smooth faciliation of rollback scenarios where we may reference previous versions of an
image. When more than 3 revisions of an asset exist in the ECR repository, the oldest one is
purged.

To change the number of revisions stored, use `imageAssetVersionCount`:

```python
app = App(
    default_stack_synthesizer=AppStagingSynthesizer.default_resources(
        app_id="my-app-id",
        image_asset_version_count=10
    )
)
```

## Using a Custom Staging Stack per Environment

If you want to customize some behavior that is not configurable via properties,
you can implement your own class that implements `IStagingResources`. To get a head start,
you can subclass `DefaultStagingStack`.

```python
class CustomStagingStack(DefaultStagingStack):
    pass
```

Or you can roll your own staging resources from scratch, as long as it implements `IStagingResources`.

```python
@jsii.implements(IStagingResources)
class CustomStagingStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation)

    def add_file(self, *, sourceHash, executable=None, fileName=None, packaging=None, deployTime=None):
        return FileStagingLocation(
            bucket_name="myBucket",
            assume_role_arn="myArn",
            dependency_stack=self
        )

    def add_docker_image(self, *, sourceHash, executable=None, directoryName=None, dockerBuildArgs=None, dockerBuildSecrets=None, dockerBuildTarget=None, dockerFile=None, repositoryName=None, networkMode=None, platform=None, dockerOutputs=None, assetName=None, dockerCacheFrom=None, dockerCacheTo=None):
        return ImageStagingLocation(
            repo_name="myRepo",
            assume_role_arn="myArn",
            dependency_stack=self
        )
```

Using your custom staging resources means implementing a `CustomFactory` class and calling the
`AppStagingSynthesizer.customFactory()` static method. This has the benefit of providing a
custom Staging Stack that can be created in every environment the CDK App is deployed to.

```python
@jsii.implements(IStagingResourcesFactory)
class CustomFactory:
    def obtain_staging_resources(self, stack, *, environmentString, deployRoleArn=None, qualifier):
        my_app = App.of(stack)

        return CustomStagingStack(my_app, f"CustomStagingStack-{context.environmentString}")

app = App(
    default_stack_synthesizer=AppStagingSynthesizer.custom_factory(
        factory=CustomFactory(),
        once_per_env=True
    )
)
```

## Using an Existing Staging Stack

Use `AppStagingSynthesizer.customResources()` to supply an existing stack as the Staging Stack.
Make sure that the custom stack you provide implements `IStagingResources`.

```python
resource_app = App()
resources = CustomStagingStack(resource_app, "CustomStagingStack")

app = App(
    default_stack_synthesizer=AppStagingSynthesizer.custom_resources(
        resources=resources
    )
)
```

## Known Limitations

Since this module is experimental, there are some known limitations:

* Currently this module does not support CDK Pipelines. You must deploy CDK Apps using this
  synthesizer via `cdk deploy`.
* This synthesizer only needs a bootstrap stack with Roles, without staging resources. We
  haven't written such a bootstrap stack yet; at the moment you can use the existing modern
  bootstrap stack, the staging resources in them will just go unused.
* Due to limitations on the CloudFormation template size, CDK Applications can have
  at most 38 independent ECR images.
* When you run `cdk destroy` (for example during testing), the staging bucket and ECR
  repositories will be left behind because CloudFormation cannot clean up non-empty resources.
  You must deploy those resources manually if you want to redeploy again using the same `appId`.
